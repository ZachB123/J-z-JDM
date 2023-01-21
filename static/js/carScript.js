
currentImage = dq(".current-image")
images = dqa(".more-images")

for (image of images) {
    image.addEventListener("click", (event) => {
        currentImage.src = event.currentTarget.src
    })
}
