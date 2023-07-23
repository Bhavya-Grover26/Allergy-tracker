const body = document.querySelector("body");
const sidebar = document.querySelector("nav");
const toggle = document.querySelector(".toggle");
const searchBox = document.querySelector(".search-box");
const modeSwitch = document.querySelector(".toggle-switch");
const modeText = document.querySelector(".mode-text");

toggle.addEventListener("click", () => {
    console.log("Toggle clicked");
    sidebar.classList.toggle("close");
});

searchBox.addEventListener("click", () => {
    console.log("Search box clicked");
    sidebar.classList.remove("close");
});

modeSwitch.addEventListener("click", () => {
    console.log("Mode switch clicked");
    body.classList.toggle("dark");
    modeText.innerText = body.classList.contains("dark")
        ? "Light Mode"
        : "Dark Mode";
});
