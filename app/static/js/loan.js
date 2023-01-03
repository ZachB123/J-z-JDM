// When the user clicks on the button toggle between hiding and showing the dropdown
dq(".credit-score-dropdown").addEventListener("click", (event) => {
    dq("#creditDropdown").classList.toggle("show");
    if (dq("#creditArrow").textContent === "arrow_drop_up") {
        dq("#creditArrow").textContent = "arrow_drop_down"
    } else {
        dq("#creditArrow").textContent = "arrow_drop_up"
    }
    event.stopPropagation()
})

window.addEventListener("click", (event) => {
    dq("#termDropdown").classList.remove("show-term");
    dq("#creditDropdown").classList.remove("show");
    dq("#creditArrow").textContent = "arrow_drop_down"
    dq("#termArrow").textContent = "arrow_drop_down"
})

// When the user clicks on the button toggle between hiding and showing the dropdown
dq(".loan-term-dropdown").addEventListener("click", (event) => {
    dq("#termDropdown").classList.toggle("show-term");
    if (dq("#termArrow").textContent === "arrow_drop_up") {
        dq("#termArrow").textContent = "arrow_drop_down"
    } else {
        dq("#termArrow").textContent = "arrow_drop_up"
    }
    event.stopPropagation()
})



// close the dropdown menu if the user clicks out of it


function creditDropdownValue () {
    
}

let loanAmount = document.querySelector("#priceInput").value;
let loanAmountSlider = document.querySelector("#priceSlider").value;
let downPayment = document.querySelector("#downPaymentSelector").value;
let tradeIn = document.querySelector("#tradeInSelector").value;


    
