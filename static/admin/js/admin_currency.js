document.addEventListener("DOMContentLoaded", () => {
    const select = document.getElementById("admin-currency-select");
    if (!select) return;
    select.addEventListener("change", async () => {
        const formData = new FormData();
        formData.append("currency", select.value);
        console.log("ewdcedc");
        
        await fetch("/set-admin-currency/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: formData,
        });

        location.reload();
    });
});

function getCookie(name) {
    return document.cookie
        .split("; ")
        .find(row => row.startsWith(name + "="))
        ?.split("=")[1];
}
