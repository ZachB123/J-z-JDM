
document.getElementById('contactUsButtonFlip').addEventListener("click", () => {
    document.getElementById('contactUsFormFront').classList.add("group-rotate-y-180");
    console.log("Nuts");
    let element = document.getElementById('contactUsFormFront');
    console.log(element);
    console.log(element.classList);
});
let element = document.getElementById('contactUsFormFront');
console.log(element);
console.log(element.classList);
// install tailwind nesting plugin






// JS for the collapsible FAQ
let coll = document.getElementsById("collapsibleFAQ");
let i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    // this.classList.toggle("active");
    // let content = this.nextElementSibling;
    // if (content.style.display === "block") {
    //   content.style.display = "hidden";
    // } else {
    //   content.style.display = "block";
    // }
    console.log("This");
  });
} 