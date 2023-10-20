class Heartbeat {

    static status = localStorage.getItem('heartbeat') === 'true';
    static _btn = document.getElementById('btn-heart');
    static _counter = document.querySelector('div#btn-heart>sub');
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
                if (this.status) {
                    this._counter.textContent = count;
                    this._btn.classList.add('beating');
                    this._counter.removeAttribute('hidden');
                }
            })

            // response took longer than 300ms
            .catch(_ => {
                if (this.status) {
                    this._counter.textContent = '⚡⚡ FIBRILLATING ⚡⚡';
                    this._btn.classList.add('fibrillating');
                    this._counter.removeAttribute('hidden');
                }
            });
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
        if (this._btn.classList.contains('fibrillating')) {
            this._btn.classList.remove('fibrillating');
            this._counter.setAttribute('hidden', 'hidden');
            this.heartbeat();
        } else {
            this.status = !this.status;
            this._set(true);
        }
    }

    static {

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