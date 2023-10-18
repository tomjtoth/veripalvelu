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

    /**
     * remove div.fun from the DOM tree after animation ends
     *
     * @param {HTMLElement} ev_target
     * @returns boolean, true if this was actually a Fun related div, else false
     */
    static rm_div(target) {
        if (target.classList.contains('fun')) {
            document.body.removeChild(target);
            return true;
        }
        return false;
    };

    static {

        // create div.fun at click pos
        document.addEventListener('click', ({ pageX, pageY }) => {
            if (this.status) new this(pageX, pageY);
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
     * creates n number of emoji at every 300ms at random x,y pos on screen
     *
     * @param {Int} n number of emoji to spam
     * @param {Int} i index of the emoji
     */
    static spam(n, i = -1) {
        if (n == 0 || !this.status) {
            this._counter.textContent = '';
            this._counter.setAttribute('hidden', 'hidden');
        } else {
            this._counter.textContent = n;
            this._counter.removeAttribute('hidden');

            setTimeout((n, i) => {
                const
                    // allowing area between (0,0) and (bottom-80,right-80)
                    w = window.screen.width - 80,
                    h = window.screen.height - 80;

                // moving above area to the center
                new this(Math.random() * w + 40, Math.random() * h + 40, i);
                this.spam(n - 1, i);
            }, 300, n, i);
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
