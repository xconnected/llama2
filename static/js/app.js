 function sendMessage() {
	var userInput = document.getElementById("user-input");
	var message = userInput.value.trim();
	if (message === "") return;

	var chatBox = document.getElementById("chat-box");
	var userDiv = document.createElement("div");
	userDiv.innerHTML = '<i class="bi bi-person-circle"></i> <strong>You:</strong> ' + message; 
	chatBox.appendChild(userDiv);

	// Clear the input field after sending the message
	document.getElementById("user-input").value = "";

	chatBox.scrollTop = chatBox.scrollHeight;

	fetch("chat", {
	    method: "POST",
	    headers: {
		"Content-Type": "application/json",
	    },
	    body: JSON.stringify({ message: message }),
	})
	    .then((response) => response.json())
	    .then((data) => {
		var botResponse = document.createElement("div");
		botResponse.innerHTML = '<i class="bi bi-cpu"></i> <strong>Llama2:</strong> ' + data.message; 
		chatBox.appendChild(botResponse);
		chatBox.scrollTop = chatBox.scrollHeight;
	    })
	    .catch((error) => {
		console.error("Error:", error);
		// Handle errors or display a failure message in the chat interface
	    });
}
