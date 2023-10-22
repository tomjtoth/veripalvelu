/**
 *  handles the FUN mode related functionalities
 */
class Fun {

    static status = localStorage.getItem('fun-mode') === 'true';
    static _emojis = [...'🤡🎉🎈🥳🎪🤹🎁🍭🤹🥳🎊'];

    static _main_content = document.querySelector('div.main-content');
    static _btn = document.querySelector('div#btn-fun');
    static _snd = {
        on: new Audio('static/sounds/party-whistle.mp3'),
        off: new Audio('static/sounds/record-scratch-with-download-link-from-youtube.mp3')
    };
    static _countdown = document.querySelector('div#btn-fun>sub');
    static _popup = document.querySelector('div.popup');

    /**
     * toggles FUN mode
     */
    static toggle(silent = false) {
        this.status = !this.status;
        if (!silent) {
            if (this.status) {
                this._snd.on.play();
            } else {
                this._snd.on.pause();
                this._snd.on.currentTime = 0;
                this._snd.off.play();
            }
        }
        this._set(true);
    }

    static _set(store_locally = false) {
        this._btn.classList[this.status ? 'add' : 'remove']('active');
        if (store_locally) localStorage.setItem('fun-mode', this.status);
    };

    static _canvas = document.createElement('div');

    static pop_up(msg, delay = 3000) {

        this._popup.innerHTML = msg.replaceAll('\n', '</br>');
        this._popup._counter++;
        this._popup.removeAttribute('hidden');

        // center horizontally
        const { width } = this._popup.getBoundingClientRect();
        this._popup.style.left = `calc(50vw - ${width}px / 2)`;

        setTimeout(_ => {
            if (--this._popup._counter == 0)
                this._popup.setAttribute('hidden', 'hidden');
        }, delay);
    }

    static rick = {
        snd: new Audio('static/sounds/Rick Roll Sound Effect.mp3'),
        img: document.createElement('img'),
        rolling: false,
        roll: function (confirm_navigation_away = false, link = null) {

            // reject multiple overlapping calls
            if (this.rolling) return;
            this.rolling = true;

            // make sure the user actually wants to navigate away :)
            if (confirm_navigation_away)
                window.onbeforeunload = () => true;


            setTimeout(_ => {
                this.snd.pause();
                this.snd.currentTime = 0;
                Fun._snd.off.play();
                this.rolling = false;
                Fun.status = false;
                Fun._set();
                if (link) link._rolled_already = true;
            }, 8.5 * 1000);

            this.toggle_theme();

            Fun.status = true;
            Fun._set();
            Fun.spam(30, 0);
            Heart.cardiac_arrest();
            this.snd.play();

            LoaderController.unhide()
        },
        toggle_theme: function () {
            setTimeout(_ => {

                if (!this.rolling) return;

                DarkModeController.toggle(false, true);
                this.toggle_theme();

            }, 1000);
        }
    }

    static trap = {
        snd: new Audio('static/sounds/itsatrap.mp3'),
        img: document.createElement('img'),
    };

    static vader = {
        snd: new Audio('static/sounds/nooo.mp3'),
        img: document.createElement('img'),
        logout_target: null,
    };

    static {

        this.rick.snd.onplay = () => {
            this.rick.img.classList.add('gliding');
        };

        this.trap.snd.onplay = () => {
            this.trap.img.style.visibility = 'visible';
        };

        this.trap.snd.onended = () => {
            this.trap.img.style.visibility = 'hidden';
        };

        this.vader.snd.onplay = () => {
            this.vader.img.style.visibility = 'visible';
        };

        this.vader.snd.onended = () => {
            this.vader.img.style.visibility = 'hidden';
            window.location = '/logout';
        }

        this._snd.on.volume = 0.15;
        this._snd.off.volume = 0.15;
        this.rick.snd.volume = 0.2;
        this.vader.snd.volume = 0.1;

        this.rick.img.classList.add('rick');
        this.rick.img.src = 'https://media.tenor.com/CHc0B6gKHqUAAAAi/deadserver.gif';
        this._main_content.appendChild(this.rick.img);

        this.trap.img.classList.add('flash-center');
        this.trap.img.src = 'https://media1.giphy.com/media/l3fZXnX7OsHuj9zDq/giphy.gif?cid=ecf05e472fzn8uauk1pbx062s2udx865bhtfm9irc61bzzug&ep=v1_gifs_search&rid=giphy.gif&ct=g';
        this._main_content.appendChild(this.trap.img);

        this.vader.img.classList.add('flash-center');
        this.vader.img.src = 'https://media.tenor.com/N0cb66tKosEAAAAC/star-wars-darth-vader.gi';
        this._main_content.appendChild(this.vader.img);

        this._popup._counter = 0;
        this._canvas.classList.add('fun-canvas');
        document.body.appendChild(this._canvas);

        this._set();

        document.addEventListener('click', (ev) => {

            const { pageX, pageY, target: { id, href, tagName, type } } = ev;

            if (this.status) {

                if (type !== 'submit' && (
                    tagName === 'INPUT'
                    || tagName === 'TEXTAREA'
                    || tagName === 'SELECT'
                )) {
                    this.trap.snd.play();
                }

                else if (
                    tagName === 'A'
                    && href.endsWith('/logout')
                ) {
                    ev.preventDefault();
                    this.vader.snd.play();
                }

                else if (
                    id !== 'btn-dark'
                    && id !== 'btn-heart'
                    && id !== 'btn-fun'
                ) new this(pageX, pageY);
            }

            if (id === 'btn-fun') {
                this.toggle();
                if (this.status) this.pop_up(
                    'satunnaisia emojeita vaan sateilee&#10;jokaisella klikkauksella'
                )
            }


        });

        document.addEventListener('animationend', ({ target }) => {
            if (target.classList.contains('fun')) {
                this._canvas.removeChild(target);
            }
            else if (target.classList.contains('rick')) {
                this.rick.img.classList.remove('gliding');
                LoaderController.hide();
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
            this._countdown.textContent = '';
            this._countdown.setAttribute('hidden', 'hidden');
        } else {
            this._countdown.textContent = n;
            this._countdown.removeAttribute('hidden');

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
