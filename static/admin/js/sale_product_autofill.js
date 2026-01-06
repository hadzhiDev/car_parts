$(document).on("select2:select", "select", function (e) {
    const select = e.target;

    if (!select.name || !select.name.endsWith("-product")) return;

    const row = select.closest("tr.form-row");
    if (!row) return;

    const productId = e.params?.data?.id;
    if (!productId) return;

    fetch(`/product-autofill/${productId}/`)
        .then(res => res.json())
        .then(data => {
            const sale_price = row.querySelector('input[name$="-sale_price"]');
            
            if (sale_price) sale_price.value = data.cost_price || "";
        });
});
