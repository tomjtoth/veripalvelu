class Fun {

    static _emojis = [...'🤡🎉🎈🥳🎪🤹‍♂️🎁🍭🤡🤹‍♀️🥳🎊'];

    static _status = localStorage.getItem('fun-mode') === 'true';

    static toggle() {
        this._status = !this._status;
        localStorage.setItem('fun-mode', this._status);
    }

    static {
        document.addEventListener('DOMContentLoaded', _ => {
            document.body.addEventListener('click', ({ pageX, pageY, target: { tagName } }) => {
                if (this._status) new this(pageX, pageY);
            });
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

    constructor(x, y) {

        const div = document.createElement('div');
        div.classList.add('fun');
        div.textContent = Fun._rand();
        div.style.left = x + 'px';
        div.style.top = y + 'px';
        document.body.appendChild(div);

    }
}
