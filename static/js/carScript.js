
currentImage = dq(".current-image")
images = dqa(".more-images")

function getImageFunction(image) {
    return () => {
        console.log(image.src)
        currentImage.src = image.src
    }
}

for (image of images) {
    func = getImageFunction(image)
    image.addEventListener("click", func)
    // image.addEventListener("click", (event) => {
    //     console.log("hello")
    //     currentImage.src = event.currentTarget.src
    // })
}

specifactionBOx
