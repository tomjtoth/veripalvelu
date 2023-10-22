class Heart {

    static status = localStorage.getItem('heartbeat') === 'true';
    static _btn = document.getElementById('btn-heart');
    static _counter = document.querySelector('div#btn-heart>sub');
    static _snd = new Audio('static/sounds/electricity_us849kj.mp3');
    /**
     * query the server how many donations are registered
     * then pulse *ONCE*
     */
    static heartbeat() {
        Promise.race([

            // query server
            fetch('/api/heartbeat'),

            // start a timer that rejects when expired
            new Promise((_resolve, reject) => setTimeout((reject) => {
                reject();
            }, 300, reject))
        ])

            // response from server arrived 1st
            .then(r => r.json()).then(count => {
                if (Fun.rick.rolling) return;

                if (this.status) {
                    this._counter.textContent = count;
                    this._btn.classList.add('beating');
                    this._counter.removeAttribute('hidden');
                }
            })

            // response took longer than 300ms
            .catch(_ => {
                if (this.status) {
                    this.cardiac_arrest();
                }
            });
    }

    static cardiac_arrest() {
        this._counter.textContent = '⚡KOHTAUS⚡';
        this._btn.classList.add('cardiac-arrest');
        this._counter.removeAttribute('hidden');
    }

    static _set(store_locally = false) {

        if (this.status) {
            this._btn.classList.add('active');
            this.heartbeat();
        } else {
            this._btn.classList.remove('active');
            this._counter.setAttribute('hidden', 'hidden');
        }
        if (store_locally) localStorage.setItem('heartbeat', this.status);

    };

    static toggle() {
        if (this._btn.classList.contains('cardiac-arrest')) {
            this._btn.classList.remove('cardiac-arrest');
            this._counter.setAttribute('hidden', 'hidden');
            this.heartbeat();
            this._snd.play();
        } else {
            this.status = !this.status;
            this._set(true);
            if (this.status) Fun.pop_up(
                'ihmisethän näkee sydämmellään parhaiten...'
                + '\n...montako luovutusta on rekisteröity järjestelmässä...'
                + '\n...REST API:n avulla ⊂(◉‿◉)つ', 5000
            );
        }
    }

    static {

        this._snd.volume = 0.2;

        this._set();

        this._btn.addEventListener('click', _ => this.toggle());

        document.addEventListener('animationend', ({ target: { id } }) => {

            // at the end of the pulse animation query the server again
            if (id == 'btn-heart') {
                this._btn.classList.remove('beating');
                if (this.status) this.heartbeat();
            }
        });
    }

}