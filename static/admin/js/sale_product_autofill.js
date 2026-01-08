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
            const article_number = row.querySelector('input[name$="-article_number"]');
            
            if (sale_price) sale_price.value = data.cost_price || "";
            if (article_number) article_number.value = data.article_number || "";
        });
});
