/* script.js */
document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("chat-form");
    const input = document.getElementById("message-input");
    const chatBox = document.getElementById("chat-box");
    const clearChatButton = document.getElementById("clear-chat");
    const videoForm = document.getElementById("video-upload-form");
    const videoFileInput = document.getElementById("video-file");
    const progressBar = document.getElementById("progress-bar");
    const transcriptionElement = document.getElementById("transcription");
    const summaryElement = document.getElementById("summary");

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const message = input.value.trim();
        if (message === "") return;

        appendMessage("Tú", message);
        input.value = "";

        fetch("/conversations/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: message }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            appendMessage("IA", data.response);
        })
        .catch(error => {
            console.error("Error:", error);
            appendMessage("IA", "Error al obtener respuesta.");
        });
    });

    clearChatButton.addEventListener("click", function() {
        chatBox.innerHTML = "";
    });

    videoForm.addEventListener("submit", function(event) {
        event.preventDefault();

        const file = videoFileInput.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append("file", file);

        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/upload_video/");

        xhr.upload.addEventListener("progress", function(event) {
            if (event.lengthComputable) {
                const percentComplete = (event.loaded / event.total) * 100;
                progressBar.style.width = percentComplete + "%";
            }
        });

        xhr.addEventListener("load", function() {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                transcriptionElement.textContent = response.transcription;
                summaryElement.textContent = response.summary;
            } else {
                console.error("Error:", xhr.statusText);
                transcriptionElement.textContent = "Error al obtener la transcripción.";
                summaryElement.textContent = "Error al obtener el resumen.";
            }
        });

        xhr.send(formData);
    });

    function appendMessage(sender, message) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message");
        messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
