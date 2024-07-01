/* script.js */
document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("chat-form");
    const input = document.getElementById("message-input");
    const chatBox = document.getElementById("chat-box");
    const uploadForm = document.getElementById("upload-form");
    const videoInput = document.getElementById("video-input");
    const progressBar = document.getElementById("progress-bar-fill");
    const clearButton = document.getElementById("clear-button");
    const resultContainer = document.getElementById("result-container");
    const loader = document.getElementById("loader");

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

    clearButton.addEventListener("click", function() {
        chatBox.innerHTML = "";
        resultContainer.innerHTML = "";
        resetProgressBar();
    });

    uploadForm.addEventListener("submit", function(event) {
        event.preventDefault();

        const file = videoInput.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append("file", file);

        loader.style.display = 'block'; // Mostrar el loader al inicio del proceso

        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/upload_video/", true);

        xhr.upload.addEventListener("progress", function(event) {
            if (event.lengthComputable) {
                const percentComplete = Math.floor((event.loaded / event.total) * 100);
                updateProgressBar(percentComplete);
            }
        });

        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                loader.style.display = 'block'; // Asegurarse de que el loader se mantenga visible
            }
        };

        xhr.send(formData);
    });

    const ws = new WebSocket("ws://localhost:8001/ws/progress");
    ws.onopen = function() {
        console.log("WebSocket connection established.");
    };

    ws.onmessage = function(event) {
        const data = JSON.parse(event.data);
        console.log("Received data:", data);
        if (data.type === "upload" || data.type === "audio" || data.type === "transcription" || data.type === "summary") {
            updateProgressBar(data.progress);
        } else if (data.type === "result") {
            loader.style.display = 'none'; // Ocultar el loader cuando se reciben los resultados
            updateProgressBar(100);
            appendMessage("Sistema", "Archivo generado correctamente.");
            displayResultOptions(data.message.file);
        }
    };

    function updateProgressBar(progress) {
        progressBar.style.width = `${progress}%`;
        progressBar.textContent = `${progress}%`;
        if (progress === 100) {
            progressBar.innerHTML = "100% ✅";
        }
    }

    function appendMessage(sender, message) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message");
        messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function displayResultOptions(filename) {
        if (!filename) return;
        const resultOptions = document.createElement("div");
        resultOptions.classList.add("result-options");
        resultOptions.innerHTML = `
            <p>Archivo generado correctamente.</p>
            <button id="view-result" class="result-button">Ver</button>
            <a href="/results/${filename}" class="result-button" download>Descargar</a>
        `;
        resultContainer.innerHTML = '';
        resultContainer.appendChild(resultOptions);

        document.getElementById("view-result").addEventListener("click", function() {
            fetch(`/results/${filename}`)
                .then(response => response.text())
                .then(text => {
                    const textArea = document.createElement("textarea");
                    textArea.value = text;
                    textArea.setAttribute("readonly", "readonly");
                    textArea.style.width = "100%";
                    textArea.style.height = "200px";
                    resultContainer.appendChild(textArea);
                });
        });
    }

    function resetProgressBar() {
        progressBar.style.width = '0%';
        progressBar.textContent = '';
    }
});
