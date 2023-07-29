
const searchButtonMobile = document.getElementById("search-button-mobile");
const searchBar = document.getElementById("search-bar");
const menuButton = document.getElementById("menu-button");
const navLinksContainer = document.getElementById("nav-links");
const navLinks = document.getElementsByClassName("nav-link");

//show/hide search bar
searchButtonMobile.addEventListener("click", (event) => {
  event.stopPropagation();
  if (searchBar.style.display === 'none') {
    searchBar.style.display = 'flex';
    searchButtonMobile.style.display = "none";
  } else {
    searchBar.style.display = 'none';
    searchButtonMobile.style.display = "block";
  }
})

//show/hide menu
menuButton.addEventListener("click", (event) => {
  event.stopPropagation();

  if(navLinksContainer.style.display === "block") {
    navLinksContainer.style.display = "none";
  } else {
    navLinksContainer.style.display = "block";
  }
})

//hide menu and searchbar if click anywhere on screen
document.addEventListener("click", (event) => {
  if(event.target !== searchBar && !searchBar.contains(event.target) && window.innerWidth < 799) {
    searchBar.style.display = "none";
    searchButtonMobile.style.display = "block";
  }
  if(event.target !== navLinksContainer && !navLinksContainer.contains(event.target) && window.innerWidth < 799) {
    navLinksContainer.style.display = "none"; 
  }
})


window.addEventListener("resize", ()=> {
  searchBar.removeAttribute("style");
  navLinksContainer.removeAttribute("style");
})

//add active class to clicked link
for (let i = 0; i < navLinks.length; i++) {
  navLinks[i].addEventListener("click", function() {
    // Remove "active" class from all links
    for (let j = 0; j < navLinks.length; j++) {
      navLinks[j].classList.remove("active");
    }
    // Add "active" class to the clicked link
    this.classList.add("active");
  });
}
