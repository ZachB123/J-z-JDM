


// the following blocks of code makes it so that the user is not able to type anything other than numbers into the input fields
let digitPeriodRegExp = new RegExp('\\d|\\.');
let input1 = document.querySelector('#priceInput');

const TAX = 0.06;

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

// the code below creates the functionality for the loan calculator
// define the variables with preset amounts
let loanAmount = 0
let sliderValue = 0
let downPayment = 0
let tradeIn = 0
let creditScore = 0
let loanTerm = 0

// change slider to have values to 160,000



loanSliderMatch()
loanInputMatch()
downPaymentMatch()
tradeInMatch()
creditScoreMatch()
loanTermMatch()

let cost = getPaymentPerMonth(loanAmount, downPayment, tradeIn, creditScore, loanTerm, 500);

loanCalculator();

// adds event listeners to each input field so that when the value changes the variable is updated
document.querySelector("#priceSlider").addEventListener("change", () => {loanSliderMatch(); loanCalculator(); });
document.querySelector("#priceInput").addEventListener("change", () => {loanInputMatch(); loanCalculator();});
document.querySelector("#downPaymentSelector").addEventListener("change", () => {downPaymentMatch(); loanCalculator();});
document.querySelector("#tradeInSelector").addEventListener("change", () => {tradeInMatch(); loanCalculator();});
document.querySelector("#creditScoreSelector").addEventListener("change", () => {creditScoreMatch(); loanCalculator();});
document.querySelector("#termDropdownSelector").addEventListener("change", () => {loanTermMatch(); loanCalculator();});

// each of these functions run when their input field triggers the event listener then they update the values
function loanSliderMatch() {
    sliderValue = Number(document.querySelector("#priceSlider").value);
    loanAmount = Number(sliderValue);
    document.querySelector("#priceInput").value = Number(sliderValue);
}
function loanInputMatch() {
    loanAmount = Number(document.querySelector("#priceInput").value);
    sliderValue = Number(loanAmount);
    document.querySelector("#priceSlider").value = Number(loanAmount);
}
function downPaymentMatch() {
    downPayment = Number(document.querySelector("#downPaymentSelector").value);
}
function tradeInMatch() {
    tradeIn = Number(document.querySelector("#tradeInSelector").value);
}
function creditScoreMatch() {
    creditScore = Number(document.querySelector("#creditScoreSelector").value);
}
function loanTermMatch() {
    loanTerm = Number(document.querySelector("#termDropdownSelector").value);
}

function loanCalculator() {
    cost = getPaymentPerMonth(loanAmount, downPayment, tradeIn, creditScore, loanTerm, 500);
    document.querySelector("#monthPriceSelector").textContent = moneyFormatter.format(+String(Math.trunc(cost)));
    document.querySelector("#budgetAmountSelector").textContent = moneyFormatter.format(String(Math.trunc(loanAmount)));
    document.querySelector("#downPaymentInfoSelector").textContent = moneyFormatter.format(String(Math.trunc(downPayment)));
    document.querySelector("#tradeValueSelector").textContent = moneyFormatter.format(String(Math.trunc(tradeIn)));
    taxRegistration = document.querySelector("#taxRegistrationSelector").textContent = moneyFormatter.format(loanAmount * TAX + 500)
    document.querySelector("#estimateAprSelector").textContent = String(Math.trunc(creditScore*100))+'%';
    document.querySelector("#totalAmountSelector").textContent = moneyFormatter.format(String(loanAmount - downPayment - tradeIn + (loanAmount * TAX + 500)));
}

function getPaymentPerMonth(carPrice, downPayment, tradeIn, rate, months, registration) {
    let totalPayment = carPrice + (carPrice * TAX) + registration - downPayment - tradeIn;
    rate = rate / 12;
    let pricePerMonth = totalPayment / ((((1 + rate) ** months) - 1) / (rate * ((1+rate) ** months)));
    return pricePerMonth;
}

function printStuff() {
    console.log(`loanAmount: ${typeof loanAmount}, ${loanAmount}`)
    console.log(`sliderValue: ${typeof sliderValue}, ${sliderValue}`)
    console.log(`downPayment: ${typeof downPayment}, ${downPayment}`)
    console.log(`tradeIn: ${typeof tradeIn}, ${tradeIn}`)
    console.log(`creditScore: ${typeof creditScore}, ${creditScore}`)
    console.log(`loanTerm: ${typeof loanTerm}, ${loanTerm}`)
}

