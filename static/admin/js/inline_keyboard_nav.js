document.addEventListener("keydown", (e) => {
    const arrows = ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"];
    if (!arrows.includes(e.key)) return;

    const target = e.target;
    if (!target.matches("input, select, textarea")) return;

    const cell = target.closest("td");
    const row = target.closest("tr");
    if (!cell || !row) return;

    e.preventDefault();

    const cells = Array.from(row.children);
    const colIndex = cells.indexOf(cell);
    const rows = Array.from(
        row.closest("tbody").querySelectorAll("tr.form-row")
    );
    const rowIndex = rows.indexOf(row);

    let nextRow = rowIndex;
    let nextCol = colIndex;

    switch (e.key) {
        case "ArrowLeft":
            nextCol--;
            break;
        case "ArrowRight":
            nextCol++;
            break;
        case "ArrowUp":
            nextRow--;
            break;
        case "ArrowDown":
            nextRow++;
            break;
    }

    const nextCell =
        rows[nextRow]?.children[nextCol];

    const nextInput =
        nextCell?.querySelector("input, select, textarea");

    if (nextInput) {
        nextInput.focus();
        nextInput.select?.();
    }
});
