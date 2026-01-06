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
            const name = row.querySelector('input[name$="-name"]');
            const article = row.querySelector('input[name$="-article_number"]');
            const cost = row.querySelector('input[name$="-cost_price"]');
            const brand = row.querySelector('select[name$="-brand"]');

            if (name) name.value = data.name || "";
            if (article ) article.value = data.article_number || "";
            if (cost) cost.value = data.cost_price || "";
            
            if (brand && data.brand_id) {
                const option = new Option(
                    data.brand_name,   // text
                    data.brand_id,     // value
                    true,              // selected
                    true               // defaultSelected
                );

                brand.append(option);
                $(brand).trigger("change");
            }

        });
});
