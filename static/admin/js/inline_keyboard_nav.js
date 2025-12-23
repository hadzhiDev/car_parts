function isAutocompleteTarget(target) {
    return (
        target.classList.contains("select2-selection") ||
        target.closest(".select2-container")
    );
}

function isSelect2Open(target) {
    const container = target.closest(".select2-container");
    return container?.classList.contains("select2-container--open");
}

function isInsideInline(target) {
    return target.closest("tr.form-row");
}

document.addEventListener("keydown", (e) => {
    const arrows = ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"];

    // ✅ ENTER → add inline
    if (e.key === "Enter") {
        if (
            isInsideInline(e.target) &&
            !isSelect2Open(e.target)
        ) {
            e.preventDefault();

            const addBtn = document.querySelector(
                ".inline-group .add-row a"
            );

            addBtn?.click();
        }
        return;
    }

    if (!arrows.includes(e.key)) return;

    const target = e.target;

    if (
        !target.matches("input, textarea") &&
        !isAutocompleteTarget(target)
    ) {
        return;
    }

    const cell = target.closest("td");
    const row = target.closest("tr.form-row");
    if (!cell || !row) return;

    e.preventDefault();

    const rows = Array.from(
        row.closest("tbody").querySelectorAll("tr.form-row")
    );

    let rowIndex = rows.indexOf(row);
    let colIndex = Array.from(row.children).indexOf(cell);

    switch (e.key) {
        case "ArrowLeft":  colIndex--; break;
        case "ArrowRight": colIndex++; break;
        case "ArrowUp":    rowIndex--; break;
        case "ArrowDown":  rowIndex++; break;
    }

    while (true) {
        const nextRow = rows[rowIndex];
        if (!nextRow) return;

        const nextCell = nextRow.children[colIndex];
        if (!nextCell) return;

        const input = nextCell.querySelector(
            "input:not([type=hidden]), textarea"
        );

        if (input && !input.disabled && !input.readOnly) {
            input.focus();
            input.select?.();
            return;
        }

        if (e.key === "ArrowRight") colIndex++;
        else if (e.key === "ArrowLeft") colIndex--;
        else if (e.key === "ArrowDown") rowIndex++;
        else if (e.key === "ArrowUp") rowIndex--;
    }
});
