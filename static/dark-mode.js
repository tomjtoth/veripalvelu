class DarkModeController {

    static status = localStorage.getItem('dark-mode') === 'true';
    static _btn = null;

    static snd = {
        light: new Audio('static/sounds/Alarm_Rooster_02.ogg'),
        dark: new Audio('static/sounds/instaowl.mp3')
    };

    static _set(store_locally = false) {

        document.documentElement.setAttribute('dark-mode', this.status);
        if (store_locally) localStorage.setItem('dark-mode', this.status);

        if (this._btn) {
            this._btn.classList[this.status ? 'add' : 'remove']('active');
        }
    };

    static toggle(store_locally = false, silent = false) {
        this.status = !this.status;
        if (!silent) {
            this.snd[this.status ? 'dark' : 'light'].play();
        }
        this._set(store_locally);
    }

    static {
        this.snd.light.volume = 0.2;
        this.snd.dark.volume = 0.5;

        this._set();

        document.addEventListener('click', ({ target: { id } }) => {

            if (id !== 'btn-dark') return;

            this.toggle(true);
        });

        document.addEventListener('DOMContentLoaded', _ => {
            this._btn = document.querySelector('div#btn-dark');
            this._set(true);
        });
    }

}
