/**
 * handles layout and color theme related dynamic functionalities
 */
class Appearance {

    // rotating circle shown during content load
    static _loader = document.querySelector('div.loader');

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

        // hide loader when pageload is done
        document.addEventListener('DOMContentLoaded', _ => {
            this._loader.setAttribute('hidden', 'hidden');
        })
    }
}
