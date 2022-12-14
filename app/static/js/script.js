
function dq(selector) {
    return document.querySelector(selector)
}

function dqa(selector) {
  return document.querySelectorAll(selector)
}

function hamburgerClick() {
    var x = document.getElementById("topnav");
    if (x.className === "navbar") {
      x.className += " responsive";
    } else {
      x.className = "navbar";
    }
}
