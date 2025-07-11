document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");

    let history = [];

    function appendMessage(role, content) {
        const msg = document.createElement("div");
        msg.className = role === "user" ? "text-right text-primary mb-2" : "text-left text-success mb-2";
        msg.innerHTML = content;
        chatBox.appendChild(msg);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    sendBtn.addEventListener("click", async () => {
        const message = userInput.value.trim();
        if (!message) return;

        appendMessage("user", message);
        userInput.value = "";

        const response = await fetch("/auth/agent_chat/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
            },
            body: JSON.stringify({ message, history })
        });

        const data = await response.json();
        appendMessage("assistant", data.response);
        history = data.history;
    });
});
