class Fun {

    static _emojis = [...'🤡🎉🎈🥳🎪🤹🎁🍭🤹🥳🎊'];

    static status = localStorage.getItem('fun-mode') === 'true';

    static _counter = document.querySelector('a[title*="fun"]>sub');

    static toggle() {
        this.status = !this.status;
        localStorage.setItem('fun-mode', this.status);
    }

    static {

        document.addEventListener('click', ({ pageX, pageY }) => {
            if (this.status) new this(pageX, pageY);
        });

        document.addEventListener('animationend', ({ target }) => {
            if (target.classList.contains('fun')) {
                document.body.removeChild(target);
            }
        });

    }

    static _rand() {
        return this._emojis[Math.floor(Math.random() * this._emojis.length)];
    }

    static err(n) {
        this._counter.textContent = n == 0 || !this.status ? '' : n;
        if (this.status && n > 0) {
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
