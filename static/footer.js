/**
 *  handles footer related dynamic functionality
 */
class Footer {

    /** adjusts the bottom margin of body according to the current height of the would-be-overlapping footer
     * 
     * @param {event} _ev
     */
    static adjust_bottom_margin(_ev) {
        const { height } = document.querySelector('body>footer').getBoundingClientRect();
        document.querySelector('body').style.marginBottom = height + 'px';
    }

    static {

        // initiate on both documentload AND resize
        document.addEventListener('DOMContentLoaded', this.adjust_bottom_margin);
        window.addEventListener('resize', this.adjust_bottom_margin);
    }
}
