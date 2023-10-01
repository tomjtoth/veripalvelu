class Fun {

    static _emojis = [...'🤡🎉🎈🥳🎪🤹🎁🍭🤹🥳🎊'];

    static status = localStorage.getItem('fun-mode') === 'true';

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
        if (this.status && n > 0) {
            setTimeout(_ => {
                new this(Math.random() * window.innerWidth, Math.random() * window.innerHeight, 0);
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
