

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

// let carousel = dqa(".carousel .car-preview-container")

// for (car of carousel) {
//     car.style.display = "none"
// }

// function setCarousel(index) {
//     carousel[index].style.display = "block"
// }

// function clearCarousel(index) {
//     carousel[index].style.display = "none"
// }

// carouselIndex = 0
// setCarousel(carouselIndex)

// let carouselLeft = dq("#carouselLeft")
// let carouselRight = dq("#carouselRight")

// carouselLeft.addEventListener("click", () => {
//     clearCarousel(carouselIndex)
//     if (carouselIndex === 0) {
//         carouselIndex = carousel.length - 1
//     } else {
//         carouselIndex = carouselIndex - 1
//     }
//     setCarousel(carouselIndex)
// })

// carouselRight.addEventListener("click", () => {
//     clearCarousel(carouselIndex)
//     if (carouselIndex === carousel.length - 1) {
//         carouselIndex = 0
//     } else {
//         carouselIndex = carouselIndex + 1
//     }
//     setCarousel(carouselIndex)
// })


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


var carousel = document.querySelector('.carousel');
var container = document.querySelector('.carousel-container');
var prevBtn = document.querySelector('.carousel-prev');
var nextBtn = document.querySelector('.carousel-next');
var pagination = document.querySelector('.carousel-pagination');
var bullets = [].slice.call(document.querySelectorAll('.carousel-bullet'));
var totalItems = document.querySelectorAll('.carousel-item').length;
var percent = (100 / totalItems);
var currentIndex = 0;

function next() {
    slideTo(currentIndex + 1);
}

function prev() {
    slideTo(currentIndex - 1);
}

function slideTo(index) {
    index = index < 0 ? totalItems - 1 : index >= totalItems ? 0 : index;
    container.style.WebkitTransform = container.style.transform = 'translate(-' + (index * percent) + '%, 0)';
    bullets[currentIndex].classList.remove('active-bullet');
    bullets[index].classList.add('active-bullet');
    currentIndex = index;
}

bullets[currentIndex].classList.add('active-bullet');
prevBtn.addEventListener('click', prev, false);
nextBtn.addEventListener('click', next, false);

pagination.addEventListener('click', function(e) {
    var index = bullets.indexOf(e.target);
    if (index !== -1 && index !== currentIndex) {
        slideTo(index);
    }
}, false);

// let svg = dqa("path")

// for (let s of svg) {
//     s.fill = "blue"
// }