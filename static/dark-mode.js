class DarkModeController {

    _set(store_locally = false) {

        document.documentElement.setAttribute(this.prop, this.status);
        if (store_locally) localStorage.setItem(this.prop, this.status);

    };

    constructor(doc_property = 'dark-mode', button_id = 'btn-dark') {

        this.status = localStorage.getItem(doc_property) === 'true';
        this.prop = doc_property;

        this._set();

        document.addEventListener('click', ({ target: { id, classList } }) => {

            if (id !== button_id) return;

            this.status = !this.status;
            if (this.status) {
                classList.add('active');
            } else {
                classList.remove('active');
            }

            this._set(true);
        });
    }

}
