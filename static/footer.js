class Footer {
    static adjust_bottom_margin(_ev) {
        const { height } = document.querySelector('body>footer').getBoundingClientRect();
        document.querySelector('body').style.marginBottom = height + 'px';
    }

    static {

        document.addEventListener('DOMContentLoaded', this.adjust_bottom_margin);
        window.addEventListener('resize', this.adjust_bottom_margin);
    }
}
