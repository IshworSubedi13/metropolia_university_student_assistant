const callerInfo = document.getElementById('callerInfo');
const callStatus = document.getElementById('callStatus');
const callTimer = document.getElementById('callTimer');
const conversation = document.getElementById('conversation');
const callBtn = document.getElementById('callBtn');
const endBtn = document.getElementById('endBtn');
const muteBtn = document.getElementById('muteBtn');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');

// State
let callActive = false;
let callStartTime = null;
let timerInterval = null;
let isMuted = false;
let sessionId = 'session_' + Date.now(); // Unique session ID per "call"

// URL Helper that works for both development and production
const getApiUrl = (endpoint) => {
    return endpoint;
};

// Add message to conversation
function addMessage(content, isAI = true) {
   const messageDiv = document.createElement('div');
   messageDiv.className = `message ${isAI ? 'ai' : 'student'}`;

   const contentDiv = document.createElement('div');
   contentDiv.className = 'message-content';
   contentDiv.textContent = content;

   messageDiv.appendChild(contentDiv);
   conversation.appendChild(messageDiv);

   conversation.scrollTop = conversation.scrollHeight;
}

// Start call timer
function startTimer() {
   callStartTime = new Date();
   timerInterval = setInterval(updateTimer, 1000);
}

// Update call timer display
function updateTimer() {
   if (!callStartTime) return;

   const now = new Date();
   const diff = Math.floor((now - callStartTime) / 1000);
   const minutes = Math.floor(diff / 60);
   const seconds = diff % 60;

   callTimer.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

// Stop call timer
function stopTimer() {
   if (timerInterval) {
      clearInterval(timerInterval);
      timerInterval = null;
   }
   callTimer.textContent = '00:00';
}

// Start a call
async function startCall() {
   if (callActive) return;

   callActive = true;
   callerInfo.textContent = 'Connected to Student Assistant AI';
   callStatus.textContent = 'Call in progress...';
   callBtn.disabled = true;
   endBtn.disabled = false;
   muteBtn.disabled = false;
   callBtn.classList.add('pulse-ring');

   startTimer();

   // Calling backend to start session using relative URL
   try {
      const response = await fetch(getApiUrl('/start_call'), {
         method: 'POST',
         headers: {
            'Content-Type': 'application/json'
         },
         body: JSON.stringify({
            session_id: sessionId
         })
      });

      if (!response.ok) {
         throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      sessionId = data.session_id;
      addMessage(data.message);
   } catch (error) {
      console.error('Start call error:', error);
      addMessage("Error starting call: " + error.message);
   }
}

// End the call
async function endCall() {
   if (!callActive) return;

   callActive = false;
   callerInfo.textContent = 'Call Ended';
   callStatus.textContent = 'Dial +18782187579 for assistance';
   callBtn.disabled = false;
   endBtn.disabled = true;
   muteBtn.disabled = true;
   callBtn.classList.remove('pulse-ring');

   stopTimer();

   // Calling backend to end session - using relative URL
   try {
      const response = await fetch(getApiUrl('/end_call'), {
         method: 'POST',
         headers: {
            'Content-Type': 'application/json'
         },
         body: JSON.stringify({
            session_id: sessionId
         })
      });

      if (!response.ok) {
         throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      addMessage(data.message);
   } catch (error) {
      console.error('End call error:', error);
      addMessage("Error ending call: " + error.message);
   }

   // Reset after a moment
   setTimeout(() => {
      callerInfo.textContent = 'Ready to Call';
      // Clear conversation except initial message
      while (conversation.children.length > 1) {
         conversation.removeChild(conversation.lastChild);
      }
      sessionId = 'session_' + Date.now();
   }, 3000);
}

function toggleMute() {
   isMuted = !isMuted;
   const micIcon = muteBtn.querySelector('.material-icons');
   micIcon.textContent = isMuted ? 'mic_off' : 'mic';
   muteBtn.style.backgroundColor = isMuted ? '#ff751f' : '#ffbd59';
   addMessage(isMuted ? "Microphone muted" : "Microphone unmuted");
}

// Send message to backend
async function sendMessage() {
   const message = messageInput.value.trim();
   if (message && callActive) {
      addMessage(message, false);
      messageInput.value = '';

      try {
         const response = await fetch(getApiUrl('/chat'), {
            method: 'POST',
            headers: {
               'Content-Type': 'application/json'
            },
            body: JSON.stringify({
               message: message,
               session_id: sessionId
            })
         });

         if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
         }

         const data = await response.json();
         if (data.response) {
            addMessage(data.response);
         } else {
            addMessage("Error: " + data.error);
         }
      } catch (error) {
         console.error('Send message error:', error);
         addMessage("Error sending message: " + error.message);
      }
   } else if (message && !callActive) {
      addMessage("Please start a call first", true);
   }
}

// Event listeners
callBtn.addEventListener('click', startCall);
endBtn.addEventListener('click', endCall);
muteBtn.addEventListener('click', toggleMute);
sendBtn.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (e) => {
   if (e.key === 'Enter') {
      sendMessage();
   }
});

// Initialize
endBtn.disabled = true;
muteBtn.disabled = true;
