let loanAmount = 20000;
let sliderValue = 20000;
let downPayment = 2000;
let tradeIn = 0;
let creditScore = .045;
let loanTerm = 72;
let cost = (((Number(loanAmount) - (Number(downPayment) + Number(tradeIn)))/Number(loanTerm))*(1+(Number(creditScore)/12)));

document.querySelector("#priceSlider").addEventListener("change", () => {loanSliderMatch(); loanCalculator(); });
document.querySelector("#priceInput").addEventListener("change", () => {loanInputMatch(); loanCalculator();});
document.querySelector("#downPaymentSelector").addEventListener("change", () => {downPaymentMatch(); loanCalculator();});
document.querySelector("#tradeInSelector").addEventListener("change", () => {tradeInMatch(); loanCalculator();});
document.querySelector("#creditScoreSelector").addEventListener("change", () => {creditScoreMatch(); loanCalculator();});
document.querySelector("#termDropdownSelector").addEventListener("change", () => {loanTermMatch(); loanCalculator();});

function loanSliderMatch() {
    sliderValue = document.querySelector("#priceSlider").value;
    loanAmount = Number(sliderValue);
    document.querySelector("#priceInput").value = '$'+sliderValue;
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



function loanCalculator() {
    cost = (((Number(loanAmount) - (Number(downPayment) + Number(tradeIn)))/Number(loanTerm))*(1+(Number(creditScore)/12)));
    document.querySelector("#monthPriceSelector").textContent = '$'+String(Math.trunc(cost));
    document.querySelector("#budgetAmountSelector").textContent = '$'+String(Math.trunc(loanAmount));
    document.querySelector("#downPaymentInfoSelector").textContent = '-$'+String(Math.trunc(downPayment));
    document.querySelector("#tradeValueSelector").textContent = '$'+String(Math.trunc(tradeIn));
    document.querySelector("#estimateAprSelector").textContent = String(Math.trunc(creditScore*100))+'%';
    document.querySelector("#totalAmountSelector").textContent = '$'+String(Math.trunc(Number(cost)*Number(loanTerm)));
    document.querySelector("#monthPriceSelectorBottom").textContent = '$'+String(Math.trunc(cost));
}