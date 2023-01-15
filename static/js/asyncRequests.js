
async function test(value) {  
    await fetch("/api/test", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({
            "value": value,
        })
    });
}

async function assign_car_to_sales_rep(salesRepId, carId) {
    await fetch("/api/assign", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({
            "carId": carId,
            "userId": salesRepId,
        })
    })
}

async function test2() {
    await fetch("/test2", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
    })
}

async function demoFlash() {
    await fetch("/api/flash", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
    })
}

async function favoriteCar(carId) {
    await fetch("/api/favorite", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({
            "car_id": carId,
        })
    })
}

async function unfavoriteCar(carId) {
    await fetch("/api/unfavorite", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({
            "car_id": carId,
        })
    })
}