const chatMain = document.getElementById('chat-main');
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');

function appendMessage(role, text) {
    const wrapper = document.createElement('div');
    wrapper.className = `chat-message ${role}`;

    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${role}`;
    bubble.textContent = text;

    wrapper.appendChild(bubble);
    chatMain.appendChild(wrapper);
    chatMain.scrollTop = chatMain.scrollHeight;
}

async function sendQuery(query) {
    const response = await fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
    });
    return response.json();
}

chatForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const query = chatInput.value.trim();
    if (!query) return;

    appendMessage('user', query);
    chatInput.value = '';

    const result = await sendQuery(query);
    if (result.error) {
        appendMessage('bot', result.error);
    } else {
        appendMessage('bot', result.answer);
    }
});
