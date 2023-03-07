
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