/**
 * handles layout and color theme related dynamic functionalities
 */
class Appearance {

    // rotating circle shown during content load
    static _loader = document.querySelector('div.loader');

    // gets assigned only when page is loaded
    static _heart = null;

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

        const color_theme = localStorage.getItem('color-theme') || 'light';
        document.documentElement.setAttribute('color-theme', color_theme);

        const path = window.location.pathname;

        for (const { title, classList, href } of document.querySelectorAll('nav>a')) {
            if (href) {
                if (href.endsWith(path)) {
                    classList.add('active');
                } else {
                    classList.remove('active');
                }
            } else {
                if (title.includes('fun') && Fun.status) {
                    classList.add('active');
                }
                else if (title.includes('dark') && color_theme == 'dark') {
                    classList.add('active');
                }
            }
        }

        document.querySelector('nav')
            .addEventListener('click', ({ target: { href, tagName, title, classList } }) => {

                if (tagName !== 'A') return;

                // show the loader if a __navigation__ link is clicked
                if (href != '') {
                    this._loader.removeAttribute('hidden');
                    return;
                }

                // handle DARK mode change/storage
                if (title.includes('dark')) {
                    const color_theme = document.documentElement
                        .getAttribute('color-theme') == 'dark'
                        ? 'light'
                        : 'dark';
                    document.documentElement.setAttribute('color-theme', color_theme);
                    localStorage.setItem('color-theme', color_theme);
                }

                // handle FUN mode change/storage
                else {
                    Fun.toggle();
                }

                classList.toggle('active');

            })

        document.addEventListener('DOMContentLoaded', _ => {

            // hide loader when pageload is done
            this._loader.setAttribute('hidden', 'hidden');

            this._heart = document.getElementById('heart');

            this._heart.addEventListener('click', _ => {
                if (this._heart.__count) {
                    alert(`There are ${this._heart.__count} donations registered`);
                }

                else {
                    alert('With each heartbeat I read how many donations are registered!');
                    // initial heartbeat
                    this.heartbeat();
                }
            });
        });

        document.addEventListener('animationend', ({ target }) => {

            if (Fun.rm_div(target)) return;

            // at the end of the pulse animation query the server again
            if (target.id == 'heart') {
                this._heart.classList.remove('beating');
                this._heart.title = 'REST API 4 the win!';
                this.heartbeat();
            }
        });

    }
}
