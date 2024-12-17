document.addEventListener("DOMContentLoaded", function () {
const dropdownToggle = document.querySelector("#profileDropdown");
const dropdownMenu = dropdownToggle.nextElementSibling;

dropdownToggle.addEventListener("click", function (e) {
e.stopPropagation();
dropdownMenu.classList.toggle("show");
});

window.addEventListener("click", function () {
dropdownMenu.classList.remove("show");
});
});
