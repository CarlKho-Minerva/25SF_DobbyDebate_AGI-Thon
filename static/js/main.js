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
    const indicator = document
      .querySelector(".user")
      .parentElement.querySelector(".status-indicator");
    indicator.classList.toggle("speaking", speaking);
    indicator.style.borderColor = speaking ? "#f04747" : "var(--secondary-bg)";
  }

  function updateDobbyStatus(speaking) {
    dobbyStatus.textContent = speaking ? "🔊 Speaking..." : "🔊 Ready";
    dobbyStatus.classList.toggle("speaking", speaking);
    const indicator = document
      .querySelector(".dobby")
      .parentElement.querySelector(".status-indicator");
    indicator.classList.toggle("speaking", speaking);
    indicator.style.borderColor = speaking ? "#3ba55c" : "var(--secondary-bg)";
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
    timer.textContent = data.seconds || "";
    if (data.seconds === 0) {
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
