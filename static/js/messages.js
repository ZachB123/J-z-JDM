
function getNumberFromUrl(url) {
    const regex = /\/(\d+)$/;
    const match = url.match(regex);
    if (match) {
      return match[1];
    }
    return null;
  }

let data;
let messageContainer = dq(".message-container")
// needed to check who the message is from
let current_user_id
let recipient_id = parseInt(getNumberFromUrl(window.location.href))

getUserId()
.then(response => response.json())
.then(data => current_user_id = parseInt(data.data.user_id))
.then(() => cycle())

function cycle() {
    getMessages(recipient_id)
    .then(response => response.json())
    .then(d => data = d)
    .then(() => {
        console.log(data.data.messages)
        messageContainer.innerHTML = ""
        insertMessages(data.data.messages)
    })
    .then(() => {
        setTimeout(() => {
          cycle();
        }, 1000);
    })
}

function insertMessages(messages) {
    for (let message of messages) {
        if (message.sender_id === current_user_id) {
            insertMessage(createMessage(message.message, "orange"))
        } else if (message.sender_id === recipient_id) {
            insertMessage(createMessage(message.message, "blue"))
        }
    }
}

function createMessage(message, color) {
    let div = document.createElement('div');
    if (color === "orange") {
        div.classList.add('message-orange');
    } else if (color === "blue") {
        div.classList.add('message-blue');
    }
  
    let p = document.createElement('p');
    p.classList.add('message-content');
    p.textContent = message;
  
    div.appendChild(p);
  
    return div;
}

function insertMessage(elem) {
    // console.log(elem)
    messageContainer.appendChild(elem)
}

