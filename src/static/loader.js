/**
 * adds a rotating circle, that's shown during content load
 */
class LoaderController {

    static _loader = document.createElement('div');

    static hide() {
        this._set_body_overflow_y();
        this._loader.setAttribute('hidden', 'hidden');
    }

    static unhide() {
        this._set_body_overflow_y('hidden');
        this._loader.removeAttribute('hidden');
    }

    static _set_body_overflow_y(value = 'auto') {
        document.body.style.overflowY = value;
    }

    static {
        this._loader.classList.add('loader');
        this._loader.appendChild(document.createElement('div'));
        this._set_body_overflow_y('hidden');
        document.body.appendChild(this._loader);

        document.addEventListener('DOMContentLoaded', _ => {
            this.hide();
        });
    }
}
