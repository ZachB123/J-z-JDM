
async function test() {
    
    let user = {
        name: 'John',
        surname: 'Smith'
    };
      
    await fetch("/test", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(user)
    });
}