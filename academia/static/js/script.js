function confirmarExclusao() {
    return window.confirm("Deseja realmente excluir este registro?");
}

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("form[data-confirm-delete='true']").forEach(function (form) {
        form.addEventListener("submit", function (event) {
            if (!confirmarExclusao()) {
                event.preventDefault();
            }
        });
    });
});
