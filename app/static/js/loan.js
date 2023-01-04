let loanAmount = 20000;
let sliderValue = 20000;
let downPayment = 2000;
let tradeIn = 0;
let creditScore = .045;
let loanTerm = 72;
let cost;

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
}
function downPaymentMatch() {
    downPayment = document.querySelector("#downPaymentSelector").value;
}
function tradeInMatch() {
    tradeIn = document.querySelector("#tradeInSelector").value;
}
function creditScoreMatch() {
    creditScore = document.querySelector("#creditScoreSelector").value;
}
function loanTermMatch() {
    loanTerm = document.querySelector("#termDropdownSelector").value;
}

document.querySelector("calculator-input").addEventListener("change", loanCalculator)

function loanCalculator() {
    let cost = (((loanAmount - (downPayment + tradeIn))/loanTerm)*(1+creditScore));
    document.querySelector("#monthPriceSelector").innerHTML = cost;
}