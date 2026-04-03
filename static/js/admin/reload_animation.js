let svg = document.getElementById("reload-svg");
let button = document.getElementById("reload-button");

button.addEventListener("click", function() {
    svg.style.transition = "transform 1s ease-in-out";
    svg.style.transform = "rotate(360deg)";

    // Nach der Animation zurücksetzen
    setTimeout(function() {
        svg.style.transition = "none";
        svg.style.transform = "rotate(0deg)";
    }, 1000);
});