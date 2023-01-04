let loanAmount = 20000;
let sliderValue = 20000;
let downPayment = 2000;
let tradeIn = 0;
let creditScore = .045;
let loanTerm = 72;
let cost = (((loanAmount - (downPayment + tradeIn))/loanTerm)*(1+creditScore));

document.querySelector("#priceSlider").addEventListener("change", loanSliderMatch);
document.querySelector("#priceInput").addEventListener("change", loanInputMatch);
document.querySelector("#downPaymentSelector").addEventListener("change", downPaymentMatch);
document.querySelector("#tradeInSelector").addEventListener("change", tradeInMatch);
document.querySelector("#creditScoreSelector").addEventListener("change", creditScoreMatch);
document.querySelector("#termDropdownSelector").addEventListener("change", loanTermMatch);

function loanSliderMatch() {
    sliderValue = document.querySelector("#priceSlider").value;
    loanAmount = Number(sliderValue);
    document.querySelector("#priceInput").value = '$'+sliderValue;
    console.log("hello"); 
}
function loanInputMatch() {
    loanAmount = document.querySelector("#priceInput").value;
    sliderValue = loanAmount;
    cost = (((loanAmount - (downPayment + tradeIn))/loanTerm)*(1+creditScore));
}
function downPaymentMatch() {
    downPayment = document.querySelector("#downPaymentSelector").value;
    cost = (((loanAmount - (downPayment + tradeIn))/loanTerm)*(1+creditScore));
}
function tradeInMatch() {
    tradeIn = document.querySelector("#tradeInSelector").value;
    cost = (((loanAmount - (downPayment + tradeIn))/loanTerm)*(1+creditScore));
}
function creditScoreMatch() {
    creditScore = document.querySelector("#creditScoreSelector").value;
    cost = (((loanAmount - (downPayment + tradeIn))/loanTerm)*(1+creditScore));
}
function loanTermMatch() {
    loanTerm = document.querySelector("#termDropdownSelector").value;
    cost = (((loanAmount - (downPayment + tradeIn))/loanTerm)*(1+creditScore));
}

document.querySelector(".input-boxes").addEventListener("change", loanCalculator);

function loanCalculator() {
    cost = (((loanAmount - (downPayment + tradeIn))/loanTerm)*(1+creditScore));
    document.querySelector("#monthPriceSelector").innerHTML = cost.toString();
    console.log("Hello")
}