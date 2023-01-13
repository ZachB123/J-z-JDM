
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
    // TODO create get request to check if current user is super user and authenticated
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