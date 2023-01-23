

carousel = [
    {
        img_src: "/static/images/bestjdmcar.jpg",
        text: "this is a very good car you shouldjhjhf buy it",
        buttonLink: "#"
    },
    {
        img_src: "/static/images/heelcar.jpg",
        text: "this is a very good car you should buy it",
        buttonLink: "#"
    },
    {
        img_src: "/static/images/honda.jpg",
        text: "this is a veryfghdfgh good car you should buy it",
        buttonLink: "#"
    },
    {
        img_src: "/static/images/hotdogcar.jpg",
        text: "this is a very good car you should buy it",
        buttonLink: "#"
    },
    {
        img_src: "/static/images/oink.jpg",
        text: "this is a very good car you should buy it",
        buttonLink: "#"
    },
]

carouselImg = dq("#carouselImg")
carouselInfo = dq("#carouselInfo")
carouselLink = dq("#carouselLink")

function setCarousel(carData) {
    carouselImg.src = carData.img_src
    carouselInfo.textContent = carData.text
    carouselLink.href = carData.buttonLink
}

setCarousel(carousel[0])
carouselIndex = 0

carouselLeft = dq("#carouselLeft")
carouselRight = dq("#carouselRight")

carouselLeft.addEventListener("click", () => {
    if (carouselIndex === 0) {
        carouselIndex = carousel.length - 1
    } else {
        carouselIndex = carouselIndex - 1
    }
    setCarousel(carousel[carouselIndex])
})

carouselRight.addEventListener("click", () => {
    if (carouselIndex === carousel.length -1) {
        carouselIndex = 0
    } else {
        carouselIndex = carouselIndex + 1
    }
    setCarousel(carousel[carouselIndex])
})

function isOpen() {
    date = new Date()
    day = date.getDay()
    hours = date.getHours()
    if ( day >= 1 && (hours >= 9 && hours <= 18)) {
        if (day === 6 && hours === 18) {
            return false
        }
        return true
    } 
    return false
}

openStatus = dq(".open-status")

if (isOpen()) {
    openStatus.textContent = "We are currently open"
} else {
    openStatus.textContent = "We are currently closed"
}

dqa(".hours > div")[new Date().getDay()].classList.add("current-day")
