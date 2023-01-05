let digitPeriodRegExp = new RegExp('\\d|\\.');
let input1 = document.querySelector('#priceInput');

input1.addEventListener('input', function(event) {
    let splitValue = input1.value.split('');
    let charactersToFilter = 0;
    let filteredSplitValue = splitValue.map(function(character) {
            if(!digitPeriodRegExp.test(character)) {
                charactersToFilter++;
                return '';
            }
        
            return character;
        });
    
    if(!charactersToFilter) {
        return;
    }
    
    input1.value = filteredSplitValue.join('');
    
    /*
     * We need to keep track of the caret position, which is the `selectionStart`
     * property, otherwise if our caret is in the middle of the value, pressing an
     * invalid character would send our caret to the end of the value.
     */
    let charactersBeforeSelectionStart = filteredSplitValue.slice(0, input1.selectionStart);
    let filteredCharactersBeforeSelectionStart = charactersBeforeSelectionStart.filter(function(character) {
            return !character;
        });
    let totalFilteredCharactersBeforeSelectionStart = filteredCharactersBeforeSelectionStart.length;
    let newSelectionStart = input1.selectionStart - totalFilteredCharactersBeforeSelectionStart;
    
    input1.selectionStart = newSelectionStart;
    input1.selectionEnd = input1.selectionStart;
}, false);

let input2 = document.querySelector('#downPaymentSelector');

input2.addEventListener('input', function(event) {
    let splitValue = input2.value.split('');
    let charactersToFilter = 0;
    let filteredSplitValue = splitValue.map(function(character) {
            if(!digitPeriodRegExp.test(character)) {
                charactersToFilter++;
                return '';
            }
        
            return character;
        });
    
    if(!charactersToFilter) {
        return;
    }
    
    input2.value = filteredSplitValue.join('');
    
    
    let charactersBeforeSelectionStart = filteredSplitValue.slice(0, input2.selectionStart);
    let filteredCharactersBeforeSelectionStart = charactersBeforeSelectionStart.filter(function(character) {
            return !character;
        });
    let totalFilteredCharactersBeforeSelectionStart = filteredCharactersBeforeSelectionStart.length;
    let newSelectionStart = input2.selectionStart - totalFilteredCharactersBeforeSelectionStart;
    
    input2.selectionStart = newSelectionStart;
    input2.selectionEnd = input2.selectionStart;
}, false);

let input3 = document.querySelector('#tradeInSelector');

input3.addEventListener('input', function(event) {
    let splitValue = input3.value.split('');
    let charactersToFilter = 0;
    let filteredSplitValue = splitValue.map(function(character) {
            if(!digitPeriodRegExp.test(character)) {
                charactersToFilter++;
                return '';
            }
        
            return character;
        });
    
    if(!charactersToFilter) {
        return;
    }
    
    input3.value = filteredSplitValue.join('');
    
    
    let charactersBeforeSelectionStart = filteredSplitValue.slice(0, input3.selectionStart);
    let filteredCharactersBeforeSelectionStart = charactersBeforeSelectionStart.filter(function(character) {
            return !character;
        });
    let totalFilteredCharactersBeforeSelectionStart = filteredCharactersBeforeSelectionStart.length;
    let newSelectionStart = input3.selectionStart - totalFilteredCharactersBeforeSelectionStart;
    
    input3.selectionStart = newSelectionStart;
    input3.selectionEnd = input3.selectionStart;
}, false);

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
    document.querySelector("#priceInput").value = Number(sliderValue);
}
function loanInputMatch() {
    loanAmount = document.querySelector("#priceInput").value;
    sliderValue = Number(loanAmount);
    document.querySelector("#priceSlider").value = Number(loanAmount);
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