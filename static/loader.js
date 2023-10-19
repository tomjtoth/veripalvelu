/**
 * adds a rotating circle, that's shown during content load
 */
class LoaderController {

    static _loader = document.createElement('div');

    static unhide() {
        this._set_overflow('hidden');
        this._loader.removeAttribute('hidden');
    }

    static _set_overflow(value = 'auto') {
        document.body.style.overflowY = value;
    }

    static {
        this._loader.classList.add('loader');
        this._loader.appendChild(document.createElement('div'));
        this._set_overflow('hidden');
        document.body.appendChild(this._loader);

        document.addEventListener('DOMContentLoaded', _ => {
            this._loader.setAttribute('hidden', 'hidden');
            this._set_overflow();
        });
    }
}
