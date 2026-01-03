(function () {

    function recalcTotals() {
        let documentTotal = 0;

        document
            .querySelectorAll('tr.form-row')
            .forEach(row => {

                const qtyInput = row.querySelector('input[name$="-quantity"]');
                if (!qtyInput) return;

                const priceInput =
                    row.querySelector('input[name$="-cost_price"]') ||
                    row.querySelector('input[name$="-sale_price"]');

                if (!priceInput) return;

                const qty = parseFloat(qtyInput.value) || 0;
                const price = parseFloat(priceInput.value) || 0;

                const rowTotal = qty * price;
                documentTotal += rowTotal;

                const totalCell = row.querySelector('.field-row_total p');
                if (totalCell) {
                    totalCell.textContent = rowTotal
                        ? rowTotal.toFixed(2)
                        : '—';
                }
            });

        const totalEl = document.getElementById('document-total');
        if (totalEl) {
            totalEl.textContent = documentTotal.toFixed(2);
        }
    }

    document.addEventListener('input', e => {
        if (
            e.target.matches('input[name$="-quantity"]') ||
            e.target.matches('input[name$="-cost_price"]') ||
            e.target.matches('input[name$="-sale_price"]')
        ) {
            recalcTotals();
        }
    });

    document.addEventListener('formset:added', recalcTotals);
    document.addEventListener('formset:removed', recalcTotals);
    document.addEventListener('DOMContentLoaded', recalcTotals);

})();
