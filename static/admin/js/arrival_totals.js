(function () {

    function recalcTotals() {
        let arrivalTotal = 0;

        document
            .querySelectorAll('tr.form-row.dynamic-items')
            .forEach(row => {

                const qtyInput = row.querySelector('input[name$="-quantity"]');
                const priceInput = row.querySelector('input[name$="-cost_price"]');

                const qty = parseFloat(qtyInput?.value) || 0;
                const price = parseFloat(priceInput?.value) || 0;

                const rowTotal = qty * price;
                arrivalTotal += rowTotal;

                const totalCell = row.querySelector('.field-row_total p');
                if (totalCell) {
                    totalCell.textContent = rowTotal
                        ? rowTotal.toFixed(2)
                        : '—';
                }
            });

        const totalEl = document.getElementById('arrival-total');
        if (totalEl) {
            totalEl.textContent = arrivalTotal.toFixed(2);
        }
    }

    // input events
    document.addEventListener('input', function (e) {
        if (
            e.target.matches('input[name$="-quantity"]') ||
            e.target.matches('input[name$="-cost_price"]')
        ) {
            recalcTotals();
        }
    });

    // inline add/remove (Django 5+)
    document.addEventListener('formset:added', recalcTotals);
    document.addEventListener('formset:removed', recalcTotals);

    document.addEventListener('DOMContentLoaded', recalcTotals);

})();
