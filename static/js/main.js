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

  button.addEventListener("click", () => {
    if (!isRecording) {
      button.disabled = true;
      updateUserStatus(true);
      socket.emit("start_recording");
    }
  });

  socket.on("recording_started", (data) => {
    updateUserStatus(true);
    timer.style.display = "block";
  });

  socket.on("timer_update", (data) => {
    const timer = document.getElementById("recordingTimer");
    if (data.seconds > 0) {
        timer.textContent = data.seconds;
        timer.style.display = "block";
    } else {
        timer.style.display = "none";
        updateUserStatus(false);
    }
  });

  socket.on("dobby_response", (data) => {
    button.disabled = false;
    updateUserStatus(false);
    timer.textContent = "";
    userTranscript.textContent = `You said: ${data.user_said}`;
    dobbyResponse.textContent = data.text;
    updateDobbyStatus(true);

    // Reset Dobby's status after speech ends
    setTimeout(() => {
      updateDobbyStatus(false);
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
  });
});
