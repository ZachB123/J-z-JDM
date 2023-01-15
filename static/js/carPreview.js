"use strict"

function previewFavoriteCar(element) {
    let carId = Number(element.getAttribute("carid"))
    let query = `button#carFavorite${Number(carId)}`
    let button = document.querySelector(query)
    button.textContent = "Unfavorite"
    button.onclick = function() { previewUnfavoriteCar(element) }
    button.id = `carUnfavorite${carId}`
    favoriteCar(carId)
}

function previewUnfavoriteCar(element) {
    let carId = Number(element.getAttribute("carid"))
    let query = `button#carUnfavorite${Number(carId)}`
    let button = dq(query)
    button.textContent = "Favorite"
    button.onclick = function() { previewFavoriteCar(element) }
    button.id = `carFavorite${carId}`
    unfavoriteCar(carId)
}

