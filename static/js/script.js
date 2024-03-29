
function dq(selector) {
    return document.querySelector(selector)
}

function dqa(selector) {
  return document.querySelectorAll(selector)
}

const toggle = document.querySelector(".hamburger-button");
const menu = document.querySelector(".list-container");
const items = document.querySelectorAll(".item");

/* Toggle mobile menu */
function toggleMenu() {
    if (menu.classList.contains("active")) {
        menu.classList.remove("active");
         
        // adds the menu (hamburger) icon
        toggle.querySelector("i").textContent = `menu`;
    } else {
        menu.classList.add("active");
         
        // adds the close (x) icon
        toggle.querySelector("i").textContent = `close`;
    }
}
 
/* Event Listener */
toggle.addEventListener("click", toggleMenu, false);
 
/* Activate Submenu */
function toggleItem() {
  if (this.classList.contains("submenu-active")) {
    this.classList.remove("submenu-active");
  } else if (menu.querySelector(".submenu-active")) {
    menu.querySelector(".submenu-active").classList.remove("submenu-active");
    this.classList.add("submenu-active");
  } else {
    this.classList.add("submenu-active");
  }
}
 
/* Event Listeners */
for (let item of items) {
    if (item.querySelector(".submenu")) {
      item.addEventListener("click", toggleItem, false);
      item.addEventListener("keypress", toggleItem, false);
    }   
}

/* Close Submenu From Anywhere */
function closeSubmenu(e) {
  if (menu.querySelector(".submenu-active")) {
    let isClickInside = menu
      .querySelector(".submenu-active")
      .contains(e.target);
 
    if (!isClickInside && menu.querySelector(".submenu-active")) {
      menu.querySelector(".submenu-active").classList.remove("submenu-active");
    }
  }
}
 
/* Event listener */
document.addEventListener("click", closeSubmenu, false);



// Adds fucntionality to the newsletter subscribe button

// Jqueury to check if the email is valid
let validateEmail = function(elementValue) {
  let emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
  return emailPattern.test(elementValue);
}
$('#email').keyup(function() {

  let value = $(this).val();
  let valid = validateEmail(value);

  if (!valid) {
      $(this).css('color', 'red');
  $('.addbut1').prop('disabled', true);
  } else {
      $(this).css('color', '#2bb673');
  $('.addbut1').prop('disabled', false);
  }
});

const newsletter = {};

newsletter.main = document.querySelector('.subscribe-email-container');
newsletter.form = document.querySelector('.subscribe-email-container > #singularForm');
newsletter.subs = document.querySelector('.subscribe-email-container > #singularForm > button#subs');
newsletter.input = document.querySelector('.subscribe-email-container>#singularForm>#emailInput>input');
newsletter.submitButton = document.querySelector('.subscribe-email-container > #singularForm > #emailInput > button');
newsletter.successMessage = document.querySelector('.subscribe-email-container > #singularForm > #success');

newsletter.submitDelay = 1000;

let sWidth = screen.width;
let buttonWidth = 0;

window.addEventListener("resize", function() {
  sWidth = screen.width;
  if (sWidth < 490) {
    buttonWidth = '20rem';
  }else if (sWidth < 580) {
    buttonWidth = '25rem';
  }else if (sWidth < 700) {
    buttonWidth = '30rem';
  } else if (sWidth < 960) {
    buttonWidth = '32rem';
  } else {
    buttonWidth = '35rem';
  }
})
if (sWidth < 490) {
  buttonWidth = '20rem';
}else if (sWidth < 580) {
  buttonWidth = '25rem';
}else if (sWidth < 700) {
  buttonWidth = '30rem';
} else if (sWidth < 960) {
  buttonWidth = '32rem';
} else {
  buttonWidth = '35rem';
}

newsletter.clickHandler = (e) => {
  switch (e.target) {
      case newsletter.subs:
          console.log('case subs');
          newsletter.main.style.width = buttonWidth;
          e.target.classList.remove('shown');
          newsletter.input.classList.add('shown');
          newsletter.submitButton.classList.add('shown');
          newsletter.input.focus();
          break;
      case newsletter.submitButton:
          newsletter.submitForm();
          break;
  }
}
newsletter.handleInputKeypress = (e) => {
  if (e.keyCode === 13) {
      e.preventDefault();
      newsletter.submitForm();
  }
}
newsletter.submitForm = () => {
  newsletter.input.style.transition = 'all .6s ease';
  newsletter.submitButton.style.transition = 'all .6s ease';
  newsletter.input.classList.remove('shown');
  newsletter.submitButton.classList.remove('shown');
  newsletter.main.style.transition = 'all .6s cubic-bezier(0.47, 0.47, 0.27, 1.20) .4s';
  newsletter.main.style.width = '';
  newsletter.successMessage.classList.add('shown');
  let submission = setTimeout(() => newsletter.form.submit(), newsletter.submitDelay);
}

newsletter.input.addEventListener('keypress', (e) => newsletter.handleInputKeypress(e));
document.addEventListener('click', (e) => newsletter.clickHandler(e));

const formatter = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
})

moneyElements = dqa(".currency")

for (elem of moneyElements) {
  elem.textContent = formatter.format(elem.textContent)
}