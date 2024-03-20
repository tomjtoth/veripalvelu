class Heart {

    static status = localStorage.getItem('heartbeat') === 'true';
    static _btn = document.getElementById('btn-heart');
    static _counter = document.querySelector('div#btn-heart>sub');
    static _snd = new Audio('static/sounds/electricity_us849kj.mp3');
    static _roundtrips = [
        // default for 1st roundtrip
        500
    ];
    static _last_query_at = null;

    static _get_avg_rndtrip() {

        // keep at most 10 trips
        if (this._roundtrips.length == 10) {
            this._roundtrips.shift();
        }

        // sum
        let total = 0;
        for (const trip of this._roundtrips) {
            total += trip;
        }

        // avg
        return total / this._roundtrips.length;
    }


    /**
     * query the server how many donations are registered
     * then pulse *ONCE*
     */
    static query_server() {

        this._last_query_at = new Date();

        Promise.race([

            // query server
            fetch('api/heartbeat'),

            // start a timer that rejects when expired
            new Promise((_resolve, reject) => setTimeout(_ => {
                reject();
            }, this._get_avg_rndtrip() + 350))
        ])

            // response from server arrived 1st
            .then(r => r.json()).then(({ count }) => {

                // append how long this roundtrip took
                this._roundtrips.push(new Date() - this._last_query_at);

                if (Fun.rick.rolling) return;

                if (this.status) {
                    this._counter.textContent = count;
                    this._btn.classList.add('beating');
                    this._counter.removeAttribute('hidden');
                }
            })

            // response took longer than the avg of last 10 + 350ms
            .catch(_ => {
                if (this.status) {
                    this._roundtrips.length = 1;
                    this._roundtrips[0] = 500;
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
            this.query_server();
        } else {
            this._btn.classList.remove('active');
            this._counter.setAttribute('hidden', 'hidden');
        }
        if (store_locally) localStorage.setItem('heartbeat', this.status);

    };

    static toggle(ev) {
        if (this._btn.classList.contains('cardiac-arrest')) {
            if (ev) {

                // create lightning bolt on top of the heart
                const l_bolt = document.createElement('div');
                l_bolt.classList.add('bolt');
                l_bolt.textContent = '⚡';
                l_bolt.style.left = ev.pageX - 8 + 'px';
                l_bolt.style.top = ev.pageY - window.scrollY - 8 + 'px';
                document.body.appendChild(l_bolt);
            }
            this._btn.classList.remove('cardiac-arrest');

            if (!this._btn.classList.contains('beating'))
                this._counter.setAttribute('hidden', 'hidden');

            this.query_server();
            this._snd.currentTime = 0;
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

        this._snd.preload = 'auto';
        this._snd.volume = 0.2;

        this._set();

        this._btn.addEventListener('click', ev => this.toggle(ev));

        document.addEventListener('animationend', ({ target }) => {

            // at the end of the pulse animation query the server again
            if (target.id == 'btn-heart') {
                this._btn.classList.remove('beating');
                if (this.status) this.query_server();
            }

            else if (target.classList.contains('bolt')) {
                document.body.removeChild(target);
            }
        });
    }
}