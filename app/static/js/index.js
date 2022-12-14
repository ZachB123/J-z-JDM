

carousel = [
    {
        img_src: "/static/images/bestcar.jpg",
        text: "this is a very good car you should buy it",
        buttonLink: "#"
    },
    {
        img_src: "/static/images/heelcar.jpg",
        text: "this is a very good car you should buy it",
        buttonLink: "#"
    },
    {
        img_src: "/static/images/honda.jpg",
        text: "this is a very good car you should buy it",
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

carouselLeft = dq("#carouselLeft")
carouselRight = dq("#carouselRight")

carouselLeft.addEventListener("click", () => {
    alert("left click")
})

carouselRight.addEventListener("click", () => {
    alert("right click")
})