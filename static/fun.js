/**
 *  handles the FUN mode related functionalities
 */
class Fun {

    static _emojis = [...'🤡🎉🎈🥳🎪🤹🎁🍭🤹🥳🎊'];

    static status = localStorage.getItem('fun-mode') === 'true';

    static _counter = document.querySelector('a[title*="fun"]>sub');

    /**
     * toggles FUN mode
     */
    static toggle() {
        this.status = !this.status;
        localStorage.setItem('fun-mode', this.status);
    }

    static {

        // create div.fun at click pos
        document.addEventListener('click', ({ pageX, pageY }) => {
            if (this.status) new this(pageX, pageY);
        });

        // remove div.fun from the DOM tree after animation ends
        document.addEventListener('animationend', ({ target }) => {
            if (target.classList.contains('fun')) {
                document.body.removeChild(target);
            }
        });

    }

    /**
     * picks 1 random emoji
     * 
     * @returns 1 emoji
     */
    static _rand() {
        return this._emojis[Math.floor(Math.random() * this._emojis.length)];
    }

    /**
     * creates 1 clown emoji at every 300ms at random x,y pos on screen
     * 
     * @param {Int} n index of the emoji
     */
    static err(n) {
        if (n == 0 || !this.status) {
            this._counter.textContent = '';
            this._counter.setAttribute('hidden', 'hidden');
        } else {
            this._counter.textContent = n;
            this._counter.removeAttribute('hidden');

            setTimeout(_ => {
                const
                    // allowing area between (0,0) and (bottom-80,right-80)
                    w = window.screen.width - 80,
                    h = window.screen.height - 80;

                // moving above area to the center
                new this(Math.random() * w + 40, Math.random() * h + 40, 0);
                this.err(n - 1);
            }, 300, n);
        }
    }

    /**
     * creates an emoji on screen at given x,y coords
     * 
     * @param {Int} x coord on screen
     * @param {Int} y coord on screen
     * @param {Int} i index of emoji, defaults to a random choice
     */
    constructor(x, y, i = -1) {

        const div = document.createElement('div');
        div.classList.add('fun');
        div.textContent = i >= 0
            ? Fun._emojis[i]
            : Fun._rand();
        div.style.left = x + 'px';
        div.style.top = y + 'px';
        document.body.appendChild(div);

    }
}
