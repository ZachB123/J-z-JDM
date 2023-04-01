
// document.getElementById('contactUsButtonFlip').addEventListener("click", () => {
//     document.getElementById('contactUsFormFront').classList.add("group-rotate-y-180");
//     console.log("Nuts");
//     let element = document.getElementById('contactUsFormFront');
//     console.log(element);
//     console.log(element.classList);
// });
// let element = document.getElementById('contactUsFormFront');
// console.log(element);
// console.log(element.classList);
// install tailwind nesting plugin



// JS for the collapsible FAQ
// let coll = document.getElementsById("collapsibleFAQ");
// let i;

// for (i = 0; i < coll.length; i++) {
//   coll[i].addEventListener("click", function() {
//     // this.classList.toggle("active");
//     // let content = this.nextElementSibling;
//     // if (content.style.display === "block") {
//     //   content.style.display = "hidden";
//     // } else {
//     //   content.style.display = "block";
//     // }
//     console.log("This");
//   });
// } 

let buttons = dqa(".faq-box button")

function getRevealFunction(elem) {
  return () => {
    elem.nextElementSibling.classList.toggle("hidden")
  }
}

for (let button of buttons) {
  button.addEventListener("click", getRevealFunction(button))
}

// let content = dqa(".FAQ-content")
// for (let box of content) {
//   box.classList.toggle("hidden")
//   box.classList.toggle("hidden")  
// }

document.addEventListener('DOMContentLoaded', function(event) {

  document.getElementById('flip-card-btn-turn-to-back').style.visibility = 'visible';
  document.getElementById('flip-card-btn-turn-to-front').style.visibility = 'visible';

  document.getElementById('flip-card-btn-turn-to-back').onclick = function() {
  document.getElementById('flip-card').classList.toggle('do-flip');
  };

  document.getElementById('flip-card-btn-turn-to-front').onclick = function() {
  document.getElementById('flip-card').classList.toggle('do-flip');
  };

});