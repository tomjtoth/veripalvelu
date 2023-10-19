class NavBar {

    static {
        const path = window.location.pathname;

        for (const { classList, href } of document.querySelectorAll('nav>a')) {
            if (href.endsWith(path)) {
                classList.add('active');
            } else {
                classList.remove('active');
            }
        }

        document.querySelector('nav')
            .addEventListener('click', ({ target: { tagName } }) => {

                if (tagName !== 'A') return;
                LoaderController.unhide();
            })
    }
}
// navlinks activated
