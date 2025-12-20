function updateInlineRowNumbers() {
    document
        .querySelectorAll('tr.form-row[id^="items-"]')
        .forEach((row) => {
            const original = row.querySelector("td.original");
            if (!original) return;

            // items-1 → 1
            const match = row.id.match(/items-(\d+)/);
            if (!match) return;

            original.textContent = match[1];
        });
}

document.addEventListener("DOMContentLoaded", updateInlineRowNumbers);
document.addEventListener("formset:added", updateInlineRowNumbers);
document.addEventListener("formset:removed", updateInlineRowNumbers);
