// Configuration
const API_BASE_URL = 'http://localhost:8000/api/v1';
const STORAGE_KEY = 'chatbot_session_id';

// State
let sessionId = null;
let messageCount = 0;
let isProcessing = false;

// DOM Elements
const chatContainer = document.getElementById('chatContainer');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const clearHistoryBtn = document.getElementById('clearHistoryBtn');
const newSessionBtn = document.getElementById('newSessionBtn');
const sessionInfo = document.getElementById('sessionInfo');
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const errorMessage = document.getElementById('errorMessage');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
});

async function initializeApp() {
    // Get or create session
    sessionId = getOrCreateSessionId();
    
    // Check API health
    await checkHealth();
    
    // Focus input
    messageInput.focus();
}

function setupEventListeners() {
    // Send button
    sendButton.addEventListener('click', handleSendMessage);
    
    // Enter key to send (Shift+Enter for new line)
    messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    });

    // Auto-resize textarea
    messageInput.addEventListener('input', () => {
        messageInput.style.height = 'auto';
        messageInput.style.height = messageInput.scrollHeight + 'px';
    });

    // Clear history
    clearHistoryBtn.addEventListener('click', handleClearHistory);
    
    // New session
    newSessionBtn.addEventListener('click', handleNewSession);
}

// ===========================
// Session Management
// ===========================

function getOrCreateSessionId() {
    let id = localStorage.getItem(STORAGE_KEY);
    if (!id) {
        id = 'session-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem(STORAGE_KEY, id);
    }
    return id;
}

// ===========================
// API Functions
// ===========================

async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            updateStatus(true, 'Connected');
            hideError();
        } else {
            updateStatus(false, 'Disconnected');
            showError('Service is currently unavailable');
        }
    } catch (error) {
        updateStatus(false, 'Disconnected');
        showError('Could not connect to server. Make sure Backend is running on port 8000');
        console.error('Health check failed:', error);
    }
}

async function sendMessageToAPI(prompt) {
    const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            prompt: prompt,
            session_id: sessionId
        })
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
}

async function clearHistory() {
    const response = await fetch(`${API_BASE_URL}/sessions/${sessionId}/clear-history`, {
        method: 'POST'
    });

    if (!response.ok) {
        throw new Error('Failed to clear history');
    }

    return await response.json();
}

async function deleteSession() {
    const response = await fetch(`${API_BASE_URL}/sessions/${sessionId}`, {
        method: 'DELETE'
    });

    if (!response.ok) {
        throw new Error('Failed to delete session');
    }

    return await response.json();
}

// ===========================
// Message Handling
// ===========================

async function handleSendMessage() {
    const message = messageInput.value.trim();
    
    if (!message || isProcessing) return;

    // Disable input
    isProcessing = true;
    sendButton.disabled = true;
    messageInput.disabled = true;

    // Display user message
    displayMessage(message, 'user');
    messageInput.value = '';
    messageInput.style.height = 'auto';

    // Show typing indicator
    showTypingIndicator();

    try {
        // Send to API
        const response = await sendMessageToAPI(message);
        
        // Hide typing indicator
        hideTypingIndicator();
        
        // Display bot response
        displayMessage(response.answer, 'bot');
        
        // Update message count
        messageCount++;
        updateSessionInfo();
        
        hideError();
    } catch (error) {
        hideTypingIndicator();
        showError('An error occurred while sending the message. Please try again.');
        console.error('Send message error:', error);
    } finally {
        // Re-enable input
        isProcessing = false;
        sendButton.disabled = false;
        messageInput.disabled = false;
        messageInput.focus();
    }
}

async function handleClearHistory() {
    if (!confirm('Do you want to clear the chat history?')) return;

    try {
        await clearHistory();
        clearChatDisplay();
        messageCount = 0;
        updateSessionInfo();
        showSuccessMessage('History cleared successfully');
    } catch (error) {
        showError('Failed to clear history');
        console.error('Clear history error:', error);
    }
}

async function handleNewSession() {
    if (!confirm('Do you want to start a new session? The current session will be deleted.')) return;

    try {
        await deleteSession();
        localStorage.removeItem(STORAGE_KEY);
        sessionId = getOrCreateSessionId();
        clearChatDisplay();
        messageCount = 0;
        updateSessionInfo();
        showSuccessMessage('New session created successfully');
    } catch (error) {
        showError('Failed to create new session');
        console.error('New session error:', error);
    }
}

// ===========================
// UI Functions
// ===========================

function displayMessage(text, sender) {
    // Remove welcome message if exists
    const welcomeMsg = chatContainer.querySelector('.welcome-message');
    if (welcomeMsg) welcomeMsg.remove();

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text;
    
    const timestamp = document.createElement('div');
    timestamp.className = 'timestamp';
    timestamp.textContent = new Date().toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
    
    contentDiv.appendChild(timestamp);
    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);
    
    scrollToBottom();
}

function showTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'typing-indicator active';
    indicator.id = 'typingIndicator';
    indicator.innerHTML = '<span></span><span></span><span></span>';
    chatContainer.appendChild(indicator);
    scrollToBottom();
}

function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) indicator.remove();
}

function clearChatDisplay() {
    chatContainer.innerHTML = `
        <div class="welcome-message">
            <h2>Welcome! 👋</h2>
            <p>Start the conversation by typing your message below</p>
        </div>
    `;
}

function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function updateStatus(isConnected, text) {
    statusDot.className = isConnected ? 'status-dot' : 'status-dot offline';
    statusText.textContent = text;
}

function updateSessionInfo() {
    sessionInfo.textContent = `Messages: ${messageCount}`;
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.add('active');
}

function hideError() {
    errorMessage.classList.remove('active');
}

function showSuccessMessage(message) {
    const successDiv = document.createElement('div');
    successDiv.style.cssText = `
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: #4CAF50;
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        z-index: 1000;
        animation: fadeIn 0.3s ease;
    `;
    successDiv.textContent = message;
    document.body.appendChild(successDiv);
    
    setTimeout(() => {
        successDiv.remove();
    }, 3000);
}