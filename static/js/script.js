function addMessage(text, sender) {
    let chatBody = document.getElementById("chatBody");

    let msgRow = document.createElement("div");
    msgRow.classList.add("message");

    let icon = document.createElement("img");
    icon.classList.add(sender === "user" ? "user-icon" : "bot-icon");
    icon.src = sender === "user"
        ? "/static/img/user_icon.jpg"
        : "/static/img/medical_bot.png";

    let bubble = document.createElement("div");
    bubble.classList.add(sender === "user" ? "user-message" : "bot-message");
    bubble.innerText = text;

    msgRow.appendChild(icon);
    msgRow.appendChild(bubble);

    chatBody.appendChild(msgRow);
    chatBody.scrollTop = chatBody.scrollHeight;
}

function sendMessage() {
    let inputField = document.getElementById("userInput");
    let message = inputField.value.trim();
    if (!message) return;

    addMessage(message, "user");
    inputField.value = "";

    fetch("/get", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
    })
    .then(res => res.json())
    .then(data => addMessage(data.bot_reply, "bot"))
    .catch(err => addMessage("Error: Unable to connect to server", "bot"));
}

/* ENTER key send */
document.getElementById("userInput").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }
});
