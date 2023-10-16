class Donation {
    static _span = document.querySelector('span#feedback');

    static {

        document.addEventListener('input', ({ target: { tagName, value } }) => {
            if (tagName !== 'TEXTAREA') return;

            this._span.textContent = value.length > 0
                ? `(${5000 - value.length} merkkiä tilaa jäljellä)`
                : '';
        });
    }
}
