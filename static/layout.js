const path = window.location.pathname;

for (const a of document.querySelectorAll('nav>a')) {
    if (a.href.endsWith(path)) {
        a.classList.add('active');
    } else {
        a.classList.remove('active');
    }
}

document.documentElement.setAttribute('color-theme',
    localStorage.getItem('color-theme') || 'light'
);

// settings
document.querySelector('nav')
    .addEventListener('click', ({ target: { href, title } }) => {

        if (href) return;

        if (title.includes('dark')) {
            const color_theme = document.documentElement
                .getAttribute('color-theme') == 'dark'
                ? 'light'
                : 'dark';
            document.documentElement.setAttribute('color-theme', color_theme);
            localStorage.setItem('color-theme', color_theme);
        }
        // FUN mode
        else {
            Fun.toggle();
        }

    })
