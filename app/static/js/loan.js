// When the user clicks on the button toggle between hiding and showing the dropdown
function creditDropdownFunction() {
    document.getElementById("creditDropdown").classList.toggle("show");
}

// close the dropdown menu if the user clicks out of it
window.onclick = function(event) {
    if (!event.target.matches('.drop-btn-credit')) {
        let dropdownsCredit = document.getElementsByClassName("credit-dropdown-content");
        let i;
        for (i = 0; i < dropdownsCredit.length; i++) {
            let openDropdownCredit = dropdownsCredit[i];
            if (openDropdownCredit.classList.contains('show')) {
                openDropdownCredit.classList.remove('show');
            }
        }
    }
}

// When the user clicks on the button toggle between hiding and showing the dropdown
function termDropdownFunction() {
    document.getElementById("termDropdown").classList.toggle("show-term");
}

// close the dropdown menu if the user clicks out of it
window.onclick = function(event) {
    if (!event.target.matches('.drop-btn-term')) {
        let dropdowns = document.getElementsByClassName("term-dropdown-content");
        let i;
        for (i = 0; i < dropdowns.length; i++) {
            let openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show-term')) {
                openDropdown.classList.remove('show-term');
            }
        }
    }
}