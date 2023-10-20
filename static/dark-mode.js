class DarkModeController {

    static status = localStorage.getItem('dark-mode') === 'true';

    static _set(classList = null, store_locally = false) {

        document.documentElement.setAttribute('dark-mode', this.status);
        if (store_locally) localStorage.setItem('dark-mode', this.status);

        if (classList) {
            classList[this.status ? 'add' : 'remove']('active');
        }
    };

    static toggle(classList = null, store_locally = false) {
        this.status = !this.status;
        this._set(classList, store_locally);
    }

    static {
        this._set();

        document.addEventListener('click', ({ target: { id, classList } }) => {

            if (id !== 'btn-dark') return;

            this.toggle(classList, true);
        });

        document.addEventListener('DOMContentLoaded', _ => {
            this._set(document.querySelector('div#btn-dark').classList, true);
        });
    }

}
