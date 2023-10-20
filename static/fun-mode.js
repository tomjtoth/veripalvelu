/**
 *  handles the FUN mode related functionalities
 */
class Fun {

    static status = localStorage.getItem('fun-mode') === 'true';

    static _emojis = [...'🤡🎉🎈🥳🎪🤹🎁🍭🤹🥳🎊'];
    static _btn = document.querySelector('div#btn-fun');
    static _counter = document.querySelector('div#btn-fun>sub');
    static _canvas = document.createElement('div');

    /**
     * toggles FUN mode
     */
    static toggle() {
        this.status = !this.status;
        this._set(true);
    }

    static _set(store_locally = false) {

        this._btn.classList[this.status
            ? 'add'
            : 'remove'
        ]('active');
        if (store_locally) localStorage.setItem('fun-mode', this.status);

    };

    static {

        this._canvas.classList.add('fun-canvas');
        document.body.appendChild(this._canvas);

        this._set();

        document.addEventListener('click', ({ pageX, pageY, target: { id } }) => {

            if (id === 'btn-fun') this.toggle();
            else if (this.status) new this(pageX, pageY);
        });

        document.addEventListener('animationend', ({ target }) => {
            if (target.classList.contains('fun')) {
                this._canvas.removeChild(target);
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
            // must reference `Fun` statically instead of `this` == this instance of Fun() 
            ? Fun._emojis[i]
            : Fun._rand();
        div.style.left = x + 'px';
        div.style.top = y - window.scrollY + 'px';
        Fun._canvas.appendChild(div);
    }
}
