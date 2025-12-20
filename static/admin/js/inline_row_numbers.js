function updateInlineRowNumbers() {
    document
        .querySelectorAll('tr.form-row[id^="items-"]')
        .forEach((row) => {
            const original = row.querySelector("td.original");
            if (!original) return;

            const match = row.id.match(/items-(\d+)/);
            if (!match) return;

            let badge = original.querySelector(".inline-row-number");
            if (!badge) {
                badge = document.createElement("span");
                badge.className = "inline-row-number";
                original.prepend(badge);
            }

            badge.textContent = match[1];
        });
}

document.addEventListener("DOMContentLoaded", updateInlineRowNumbers);
document.addEventListener("formset:added", updateInlineRowNumbers);
document.addEventListener("formset:removed", updateInlineRowNumbers);
