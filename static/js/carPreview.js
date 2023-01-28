"use strict"

function previewFavoriteCar(element) {
    let carId = Number(element.getAttribute("carid"))
    let query = `button#carFavorite${Number(carId)}`
    let button = document.querySelector(query)
    button.querySelector("i").textContent = "bookmark_remove"
    button.querySelector("i").classList.remove("favorite")
    button.querySelector("i").classList.add("unfavorite")
    button.onclick = function() { previewUnfavoriteCar(element) }
    button.id = `carUnfavorite${carId}`
    favoriteCar(carId)
}

function previewUnfavoriteCar(element) {
    let carId = Number(element.getAttribute("carid"))
    let query = `button#carUnfavorite${Number(carId)}`
    let button = dq(query)
    button.querySelector("i").textContent = "bookmark_add"
    button.querySelector("i").classList.add("favorite")
    button.querySelector("i").classList.remove("unfavorite")
    button.onclick = function() { previewFavoriteCar(element) }
    button.id = `carFavorite${carId}`
    unfavoriteCar(carId)
}

const moneyFormatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  });

let priceTags = dqa(".currency")

for (let price of priceTags) {
    let content = price.textContent
    price.textContent = moneyFormatter.format(content)
}


