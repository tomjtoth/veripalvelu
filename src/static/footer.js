/**
 *  handles footer related dynamic functionality
 */
class Footer {

    /** adjusts the bottom margin of body according to the current height of the would-be-overlapping footer
     *
     * @param {event} _ev
     */
    static _adjust_bottom_margin(_ev) {
        const footer = document.querySelector('div.main-content>footer');
        const { paddingTop, paddingBottom, height } = window.getComputedStyle(footer);
        document.querySelector('body').style.marginBottom =
            `calc(${height} + ${paddingTop} + ${paddingBottom} + 5vh)`;
    }

    static {

        // initiate on both documentload AND resize
        document.addEventListener('DOMContentLoaded', this._adjust_bottom_margin);
        window.addEventListener('resize', this._adjust_bottom_margin);
    }
}
