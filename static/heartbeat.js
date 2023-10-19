class Heartbeat {

    static _heart = document.getElementById('btn-heart');
    /**
     * query the server how many donations are registered
     * then pulse *ONCE*
     */
    static heartbeat() {
        fetch('/api/heartbeat').then(r => r.json()).then(count => {
            this._heart.__count = count;
            this._heart.classList.add('beating');
        });
    }

    static {


        this._heart.addEventListener('click', _ => {
            if (this._heart.__count) {
                alert(`On ${this._heart.__count} luovutusta rekisteröity`);
            }

            else {
                alert('Jokaisella sykkeellä luen montako luovutus on rekisteröity!');
                // initial heartbeat
                this.heartbeat();
                this._heart.classList.add('active');
            }
        });

        document.addEventListener('animationend', ({ target: { id } }) => {

            // at the end of the pulse animation query the server again
            if (id == 'btn-heart') {
                this._heart.classList.remove('beating');
                this._heart.title = 'REST API ftw!';
                this.heartbeat();
            }
        });
    }

}