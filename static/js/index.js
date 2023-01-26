

// carousel = [
//     {
//         img_src: "/static/images/bestjdmcar.jpg",
//         text: "this is a very good car you shouldjhjhf buy it",
//         buttonLink: "#"
//     },
//     {
//         img_src: "/static/images/heelcar.jpg",
//         text: "this is a very good car you should buy it",
//         buttonLink: "#"
//     },
//     {
//         img_src: "/static/images/honda.jpg",
//         text: "this is a veryfghdfgh good car you should buy it",
//         buttonLink: "#"
//     },
//     {
//         img_src: "/static/images/hotdogcar.jpg",
//         text: "this is a very good car you should buy it",
//         buttonLink: "#"
//     },
//     {
//         img_src: "/static/images/oink.jpg",
//         text: "this is a very good car you should buy it",
//         buttonLink: "#"
//     },
// ]

// carouselImg = dq("#carouselImg")
// carouselInfo = dq("#carouselInfo")
// carouselLink = dq("#carouselLink")

let carousel = dqa(".carousel .car-preview-container")

for (car of carousel) {
    car.style.display = "none"
}

function setCarousel(index) {
    carousel[index].style.display = "block"
}

function clearCarousel(index) {
    carousel[index].style.display = "none"
}

carouselIndex = 0
setCarousel(carouselIndex)

let carouselLeft = dq("#carouselLeft")
let carouselRight = dq("#carouselRight")

carouselLeft.addEventListener("click", () => {
    clearCarousel(carouselIndex)
    if (carouselIndex === 0) {
        carouselIndex = carousel.length - 1
    } else {
        carouselIndex = carouselIndex - 1
    }
    setCarousel(carouselIndex)
})

carouselRight.addEventListener("click", () => {
    clearCarousel(carouselIndex)
    if (carouselIndex === carousel.length - 1) {
        carouselIndex = 0
    } else {
        carouselIndex = carouselIndex + 1
    }
    setCarousel(carouselIndex)
})


function isOpen() {
    let date = new Date()
    let day = date.getDay()
    let hours = date.getHours()
    if ( day >= 1 && (hours >= 9 && hours < 18)) {
        if (day === 6 && hours === 18) {
            return false
        }
        return true
    } 
    return false
}

let openStatus = dq(".open-status")

if (isOpen()) {
    openStatus.textContent = "We are currently open"
} else {
    openStatus.textContent = "We are currently closed"
}

dqa(".hours > div")[new Date().getDay()].classList.add("current-day")
