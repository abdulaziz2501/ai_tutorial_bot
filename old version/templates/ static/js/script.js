/**
 * AI Tutoring Bot - Frontend JavaScript
 * Chat funksionalligini boshqaradi
 */

// Global o'zgaruvchilar
const API_BASE_URL = 'http://localhost:5000/api';
let sessionId = generateSessionId();
let currentQuiz = null;

// DOM elementlari
const welcomeScreen = document.getElementById('welcomeScreen');
const chatMessages = document.getElementById('chatMessages');
const inputArea = document.getElementById('inputArea');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const startBtn = document.getElementById('startBtn');
const suggestions = document.getElementById('suggestions');
const progressModal = document.getElementById('progressModal');
const progressBtn = document.getElementById('progressBtn');
const closeModal = document.getElementById('closeModal');
const resetBtn = document.getElementById('resetBtn');
const loading = document.getElementById('loading');

// Event listeners
startBtn.addEventListener('click', startChat);
sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', handleEnterKey);
userInput.addEventListener('input', autoResize);
progressBtn.addEventListener('click', showProgress);
closeModal.addEventListener('click', hideProgress);
resetBtn.addEventListener('click', resetChat);

// Topic items
document.querySelectorAll('.topic-item').forEach(item => {
    item.addEventListener('click', () => {
        const topic = item.dataset.topic;
        const topicText = item.querySelector('span').textContent;
        sendMessage(topicText);
    });
});

/**
 * Session ID generatsiya qilish
 */
function generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

/**
 * Chatni boshlash
 */
function startChat() {
    welcomeScreen.style.display = 'none';
    chatMessages.style.display = 'flex';
    inputArea.style.display = 'block';
    
    // Birinchi xabarni yuborish
    sendMessage('salom');
}

/**
 * Xabar yuborish
 */
async function sendMessage(messageText = null) {
    const message = messageText || userInput.value.trim();
    
    if (!message) return;
    
    // User xabarini ko'rsatish
    addMessage(message, 'user');
    
    // Inputni tozalash
    userInput.value = '';
    autoResize();
    
    // Loadingni ko'rsatish
    showLoading();
    
    try {
        // API ga so'rov yuborish
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Bot javobini ko'rsatish
            addMessage(data.response.message, 'bot');
            
            // Tavsiyalarni ko'rsatish
            if (data.response.suggestions) {
                showSuggestions(data.response.suggestions);
            }
            
            // Agar quiz bo'lsa, saqlash
            if (data.response.type === 'quiz' && data.response.quiz) {
                currentQuiz = data.response.quiz;
            }
        } else {
            addMessage('Xatolik yuz berdi: ' + data.error, 'bot');
        }
    } catch (error) {
        console.error('Error:', error);
        addMessage('Server bilan bog\'lanishda xatolik yuz berdi.', 'bot');
    } finally {
        hideLoading();
    }
}

/**
 * Xabar qo'shish
 */
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = sender === 'bot' ? '<i class="fas fa-robot"></i>' : '<i class="fas fa-user"></i>';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    // Markdown va kod bloklarini qayta ishlash
    content.innerHTML = formatMessage(text);
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Xabarni formatlash (Markdown support)
 */
function formatMessage(text) {
    // Code blocks
    text = text.replace(/```python\n([\s\S]*?)\n```/g, '<pre><code>$1</code></pre>');
    text = text.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
    
    // Inline code
    text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
    
    // Bold
    text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    
    // Headers
    text = text.replace(/^### (.+)$/gm, '<h3>$1</h3>');
    text = text.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    text = text.replace(/^# (.+)$/gm, '<h1>$1</h1>');
    
    // Lists
    text = text.replace(/^- (.+)$/gm, '<li>$1</li>');
    text = text.replace(/^• (.+)$/gm, '<li>$1</li>');
    
    // Wrap lists
    text = text.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');
    
    // Line breaks
    text = text.replace(/\n\n/g, '<br><br>');
    text = text.replace(/\n/g, '<br>');
    
    return text;
}

/**
 * Tavsiyalarni ko'rsatish
 */
function showSuggestions(suggestionsList) {
    suggestions.innerHTML = '';
    
    suggestionsList.forEach(suggestion => {
        const chip = document.createElement('div');
        chip.className = 'suggestion-chip';
        chip.textContent = suggestion;
        chip.addEventListener('click', () => {
            sendMessage(suggestion);
        });
        suggestions.appendChild(chip);
    });
}

/**
 * Enter tugmasini bosish
 */
function handleEnterKey(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}

/**
 * Textarea avtomatik o'lchamini o'zgartirish
 */
function autoResize() {
    userInput.style.height = 'auto';
    userInput.style.height = userInput.scrollHeight + 'px';
}

/**
 * Progressni ko'rsatish
 */
async function showProgress() {
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE_URL}/progress?session_id=${sessionId}`);
        const data = await response.json();
        
        if (data.success) {
            const progress = data.progress;
            
            document.getElementById('topicsLearned').textContent = progress.topics_learned;
            document.getElementById('quizzesCompleted').textContent = progress.quizzes_completed;
            document.getElementById('correctAnswers').textContent = progress.correct_answers;
            document.getElementById('accuracy').textContent = progress.accuracy.toFixed(1) + '%';
            
            progressModal.classList.add('active');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Progressni yuklashda xatolik yuz berdi.');
    } finally {
        hideLoading();
    }
}

/**
 * Progress modalini yopish
 */
function hideProgress() {
    progressModal.classList.remove('active');
}

/**
 * Chatni qayta boshlash
 */
async function resetChat() {
    if (!confirm('Haqiqatan ham chatni qayta boshlamoqchimisiz? Barcha progress yo\'qoladi.')) {
        return;
    }
    
    showLoading();
    
    try {
        await fetch(`${API_BASE_URL}/reset`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: sessionId
            })
        });
        
        // Yangi session boshlash
        sessionId = generateSessionId();
        chatMessages.innerHTML = '';
        suggestions.innerHTML = '';
        currentQuiz = null;
        
        // Welcome screen'ga qaytish
        chatMessages.style.display = 'none';
        inputArea.style.display = 'none';
        welcomeScreen.style.display = 'flex';
        
    } catch (error) {
        console.error('Error:', error);
        alert('Resetlashda xatolik yuz berdi.');
    } finally {
        hideLoading();
    }
}

/**
 * Loadingni ko'rsatish
 */
function showLoading() {
    loading.style.display = 'flex';
    sendBtn.disabled = true;
}

/**
 * Loadingni yashirish
 */
function hideLoading() {
    loading.style.display = 'none';
    sendBtn.disabled = false;
}

/**
 * Modal tashqarisiga bosganda yopish
 */
progressModal.addEventListener('click', (e) => {
    if (e.target === progressModal) {
        hideProgress();
    }
});

/**
 * Quiz javobini tekshirish
 */
async function checkQuizAnswer(answer) {
    if (!currentQuiz) return;
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE_URL}/quiz/check`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                quiz: currentQuiz,
                answer: answer,
                session_id: sessionId
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            addMessage(data.result.message, 'bot');
            currentQuiz = null;
        }
    } catch (error) {
        console.error('Error:', error);
        addMessage('Javobni tekshirishda xatolik yuz berdi.', 'bot');
    } finally {
        hideLoading();
    }
}

/**
 * Raqam kirganini tekshirish (quiz javoblari uchun)
 */
userInput.addEventListener('keypress', (e) => {
    if (currentQuiz && e.key >= '1' && e.key <= '4') {
        e.preventDefault();
        const answer = e.key;
        userInput.value = answer;
        sendBtn.click();
    }
});

// Health check
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        console.log('Server status:', data);
    } catch (error) {
        console.error('Server is not running:', error);
    }
}

// Sahifa yuklanganda health check
window.addEventListener('load', checkHealth);

console.log('🤖 AI Tutoring Bot initialized!');
console.log('Session ID:', sessionId);
