document.addEventListener("DOMContentLoaded", () => {
  const socket = io({
    transports: ["websocket"],
    pingTimeout: 60000,
  });

  const button = document.getElementById("startDebate");
  const userStatus = document.getElementById("userStatus");
  const dobbyStatus = document.getElementById("dobbyStatus");
  const timer = document.getElementById("recordingTimer");
  const userTranscript = document.getElementById("userTranscript");
  const dobbyResponse = document.getElementById("dobbyResponse");

  let isRecording = false;

  const debateTopics = [
    "Web3 is the future of the internet",
    "AI will replace all developers by 2030",
    "Remote work is killing innovation",
    "Bitcoin is digital gold",
    "DeFi will replace traditional banking",
    "NFTs are a scam",
    "Social media is destroying society",
    "Universities are obsolete",
    "The Metaverse will fail",
    "Apple is just a marketing company now"
  ];

  function getRandomTopic() {
    return debateTopics[Math.floor(Math.random() * debateTopics.length)];
  }

  const randomTopicBtn = document.getElementById('randomTopic');
  const startDebateBtn = document.getElementById('startDebate');
  const currentTopicEl = document.getElementById('currentTopic');

  function updateTopic() {
    const newTopic = getRandomTopic();
    currentTopicEl.textContent = newTopic;
    startDebateBtn.disabled = false;
    return newTopic;
  }

  randomTopicBtn.addEventListener('click', () => {
    const topic = updateTopic();
    console.log('New topic:', topic);
  });

  // Initial random topic
  updateTopic();

  function updateUserStatus(speaking) {
    isRecording = speaking;
    userStatus.textContent = speaking ? "🎙️ Speaking..." : "🎙️ Ready";
    userStatus.classList.toggle("speaking", speaking);
    const userWrapper = document.querySelector(".user-wrapper");
    userWrapper.classList.toggle("speaking", speaking);
  }

  function updateDobbyStatus(speaking) {
    dobbyStatus.textContent = speaking ? "🔊 Speaking..." : "🔊 Ready";
    dobbyStatus.classList.toggle("speaking", speaking);
    const dobbyWrapper = document.querySelector(".dobby-wrapper");
    dobbyWrapper.classList.toggle("speaking", speaking);
  }

  const overlay = document.getElementById('timerOverlay');
  const timerDisplay = document.querySelector('.timer-display');

  button.addEventListener("click", () => {
    if (!isRecording && !button.disabled) {
        isRecording = true;
        button.disabled = true;
        userStatus.textContent = '🎙️ Recording...';
        button.classList.add('recording');

        // Show overlay with timer
        overlay.classList.add('active');
        let timeLeft = 5;

        const countdown = setInterval(() => {
            timerDisplay.textContent = timeLeft;
            timeLeft--;

            if (timeLeft < 0) {
                clearInterval(countdown);
                overlay.classList.remove('active');
                isRecording = false;
                userStatus.textContent = '🎙️ Ready';
                button.classList.remove('recording');
            }
        }, 1000);

        socket.emit('start_recording');
    }
  });

  socket.on("recording_started", (data) => {
    timer.textContent = '5s';
  });

  socket.on("timer_update", (data) => {
    timer.textContent = data.seconds > 0 ? `${data.seconds}s` : '';
  });

  socket.on("dobby_response", (data) => {
    updateUserStatus(false);
    timer.textContent = "";
    userTranscript.textContent = `You: ${data.user_said}`;
    dobbyResponse.textContent = `Dobby: ${data.text}`;
    dobbyResponse.classList.add('speaking');
    updateDobbyStatus(true);

    setTimeout(() => {
        updateDobbyStatus(false);
        button.disabled = false;  // Re-enable button after Dobby responds
        dobbyResponse.classList.remove('speaking');
        overlay.classList.remove('active');
    }, 5000);
  });

  socket.on("connect_error", (error) => {
    console.error("Connection error:", error);
    button.disabled = false;
    updateUserStatus(false);
  });

  socket.on("error", (data) => {
    console.error("Server error:", data.message);
    button.disabled = false;
    updateUserStatus(false);
    userStatus.textContent = '❌ Error';
    setTimeout(() => {
        userStatus.textContent = '🎙️ Ready';
    }, 2000);
  });

  // Initialize with disabled speak button
  document.getElementById('startDebate').disabled = true;

  document.getElementById('randomTopic').addEventListener('click', updateTopic);
});
