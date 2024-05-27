 async function sendMessage() {
            const messageInput = document.getElementById('message');
            const message = messageInput.value;
            addMessage('User', message);
            messageInput.value = '';

            addTypingIndicator();

            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });
            const data = await response.json();

            removeTypingIndicator();
            setTimeout(() => {
                addMessage('Bot', data.response);
                addMessagePopUp('Bot', data.response); // Call the pop-up function
            }, 1000); // Simulate typing delay
        }

        function addMessage(sender, text) {
            const messagesContainer = document.getElementById('messages');
            const messageElement = document.createElement('div');
            messageElement.classList.add('message');
            messageElement.innerHTML = `<strong>${sender}:</strong> ${text}`;
            messagesContainer.appendChild(messageElement);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        function addTypingIndicator() {
            const messagesContainer = document.getElementById('messages');
            const typingIndicator = document.createElement('div');
            typingIndicator.id = 'typing-indicator';
            typingIndicator.classList.add('message', 'typing');
            typingIndicator.innerText = 'Bot is typing...';
            messagesContainer.appendChild(typingIndicator);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        function removeTypingIndicator() {
            const typingIndicator = document.getElementById('typing-indicator');
            if (typingIndicator) {
                typingIndicator.remove();
            }
        }

        // Function to greet user when chatbot is loaded
        function greetUser() {
            addMessage('Bot', 'Hi There! My Name is Geo, I am a Chatbot designed to provide you information about GeoCities. To continue, you can type "Hello"');
        }

        document.addEventListener('DOMContentLoaded', () => {
            greetUser(); // Call greetUser function when the page is loaded

            const messageInput = document.getElementById('message');
            messageInput.addEventListener('keyup', (event) => {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            });
        });