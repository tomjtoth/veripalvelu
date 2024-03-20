/**
 * handle donation related dynamic functionalities
 */
class Donation {
    static _span = document.querySelector('span#feedback');
    static _snd = new Audio('static/sounds/tada_1.mp3');
    static dates = null;
    static _submit_target = null;

    static {

        this._snd.preload = 'auto';

        fetch('api/dates').then(r => r.json()).then(dates => {
            this.dates = dates;
        });

        this._snd.volume = 0.05;
        this._snd.onended = () => {
            this._submit_target.dispatchEvent(new Event('submit'));
        }

        // update feedback to user on length of remaining chars
        document.addEventListener('input', ({ target: { tagName, value } }) => {
            if (tagName !== 'TEXTAREA') return;

            this._span.textContent = value.length > 0
                ? `(${5000 - value.length} merkkiä tilaa jäljellä)`
                : '';
        });

        document.addEventListener('click', ({ target: { classList, tagName } }) => {
            if (classList.contains('easter-egg') && tagName == 'SPAN') {
                Fun.rick.roll();
            }
        });

        document.addEventListener('submit', async function (ev) {

            const ddate = new Date(document.querySelector('input[type=date]').value);

            const conflicting_date = Donation.dates.find(date_str => {
                const existing_date = new Date(date_str);
                if (Math.abs(ddate - existing_date) < 1000 * 60 * 60 * 24 * 90)
                    return existing_date;
            });

            if (conflicting_date) {
                ev.preventDefault();
                alert(
                    'Toinen luovutus 90 pv:n sisällä:\n'
                    + new Date(conflicting_date).toLocaleDateString()
                    + '\net voinut silloin luovuttaa!'
                );
                return;
            }

            if (Fun.status && !this._submit_target) {
                ev.preventDefault();
                Donation._snd.play();
                Donation._submit_target = ev.target;
            }
        });
    }
}
