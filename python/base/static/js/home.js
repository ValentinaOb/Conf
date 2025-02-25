document.addEventListener("DOMContentLoaded", function () {
    let profile = document.getElementById("profile");
    let menu = document.getElementById("menu");

    // Show menu on hover
    profile.addEventListener("mouseenter", function () {
        menu.style.display = "block";
    });

    // Keep menu open when hovering over it
    menu.addEventListener("mouseenter", function () {
        menu.style.display = "block";
    });

    // Hide menu when the mouse leaves the profile or menu
    menu.addEventListener("mouseleave", function () {
        menu.style.display = "none";
    });

    profile.addEventListener("mouseleave", function () {
        setTimeout(function () {
            if (!menu.matches(":hover")) {
                menu.style.display = "none";
            }
        }, 300);
    });
});