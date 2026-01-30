// Chat state
let isGenerating = false;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('userInput');
    
    // Handle Enter key
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Auto-resize textarea
    userInput.addEventListener('input', () => {
        userInput.style.height = 'auto';
        userInput.style.height = userInput.scrollHeight + 'px';
    });
    
    // Check health
    checkHealth();
});

function checkHealth() {
    fetch('/api/health')
        .then(res => res.json())
        .then(data => {
            console.log('Service healthy:', data);
        })
        .catch(err => {
            console.error('Health check failed:', err);
            addSystemMessage('⚠️ Warning: Could not connect to the AI service. Please ensure Ollama is running.');
        });
}

function insertCommand(command) {
    const input = document.getElementById('userInput');
    input.value = command;
    input.focus();
}

function showCommandHelp(type) {
    const helpMessages = {
        explain: "To explain Stata code, type:\n/explain regress y x1 x2",
        fix: "To fix Stata code, type:\n/fix [your code here]",
        optimize: "To optimize Stata code, type:\n/optimize [your code here]",
        general: "Just type any Stata question or code, and I'll help!"
    };
    
    addSystemMessage(helpMessages[type]);
}

function addSystemMessage(content) {
    const chatContainer = document.getElementById('chatContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-label">System</div>
            ${content}
        </div>
    `;
    
    // Remove welcome message if exists
    const welcome = chatContainer.querySelector('.welcome-message');
    if (welcome) welcome.remove();
    
    chatContainer.appendChild(messageDiv);
    scrollToBottom();
}

function addUserMessage(content) {
    const chatContainer = document.getElementById('chatContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user';
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-label">You</div>
            ${escapeHtml(content)}
        </div>
    `;
    
    // Remove welcome message if exists
    const welcome = chatContainer.querySelector('.welcome-message');
    if (welcome) welcome.remove();
    
    chatContainer.appendChild(messageDiv);
    scrollToBottom();
    return messageDiv;
}

function addAssistantMessage() {
    const chatContainer = document.getElementById('chatContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-label">Llama 3.2</div>
            <span class="content"></span>
        </div>
    `;
    
    chatContainer.appendChild(messageDiv);
    scrollToBottom();
    return messageDiv;
}

async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();
    
    if (!message || isGenerating) return;
    
    // Add user message
    addUserMessage(message);
    
    // Clear input
    userInput.value = '';
    userInput.style.height = 'auto';
    
    // Update button state
    setGenerating(true);
    
    // Check if it's a command
    const commandMatch = message.match(/^\/(explain|fix|optimize)\s+(.+)$/s);
    
    if (commandMatch) {
        const [, command, code] = commandMatch;
        await handleCommand(command, code);
    } else {
        await handleChat(message);
    }
    
    setGenerating(false);
}

async function handleChat(message) {
    const assistantMsg = addAssistantMessage();
    const contentSpan = assistantMsg.querySelector('.content');
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message })
        });
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop();
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = JSON.parse(line.slice(6));
                    
                    if (data.error) {
                        contentSpan.innerHTML = `<span style="color: red;">Error: ${escapeHtml(data.error)}</span>`;
                        return;
                    }
                    
                    if (data.content) {
                        contentSpan.textContent += data.content;
                        scrollToBottom();
                    }
                    
                    if (data.done) {
                        // Format the final message with markdown
                        contentSpan.innerHTML = formatMessage(contentSpan.textContent);
                    }
                }
            }
        }
    } catch (error) {
        contentSpan.innerHTML = `<span style="color: red;">Error: ${escapeHtml(error.message)}</span>`;
    }
}

async function handleCommand(command, code) {
    const assistantMsg = addAssistantMessage();
    const contentSpan = assistantMsg.querySelector('.content');
    
    try {
        const response = await fetch(`/api/commands/${command}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code })
        });
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop();
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = JSON.parse(line.slice(6));
                    
                    if (data.error) {
                        contentSpan.innerHTML = `<span style="color: red;">Error: ${escapeHtml(data.error)}</span>`;
                        return;
                    }
                    
                    if (data.content) {
                        contentSpan.textContent += data.content;
                        scrollToBottom();
                    }
                    
                    if (data.done) {
                        // Format the final message
                        contentSpan.innerHTML = formatMessage(contentSpan.textContent);
                    }
                }
            }
        }
    } catch (error) {
        contentSpan.innerHTML = `<span style="color: red;">Error: ${escapeHtml(error.message)}</span>`;
    }
}

function setGenerating(generating) {
    isGenerating = generating;
    const sendBtn = document.getElementById('sendBtn');
    const btnText = document.getElementById('sendBtnText');
    const btnSpinner = document.getElementById('sendBtnSpinner');
    
    sendBtn.disabled = generating;
    btnText.style.display = generating ? 'none' : 'inline';
    btnSpinner.style.display = generating ? 'inline-block' : 'none';
}

function scrollToBottom() {
    const chatContainer = document.getElementById('chatContainer');
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatMessage(text) {
    // Basic markdown-like formatting
    let formatted = escapeHtml(text);
    
    // Code blocks
    formatted = formatted.replace(/```([^`]+)```/g, '<pre><code>$1</code></pre>');
    
    // Inline code
    formatted = formatted.replace(/`([^`]+)`/g, '<code>$1</code>');
    
    // Bold
    formatted = formatted.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    
    // Line breaks
    formatted = formatted.replace(/\n/g, '<br>');
    
    return formatted;
}
