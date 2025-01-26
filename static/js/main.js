document.addEventListener("DOMContentLoaded", () => {
  const socket = io();
  const button = document.getElementById("startDebate");
  const userStatus = document.getElementById("userStatus");
  const dobbyStatus = document.getElementById("dobbyStatus");
  const timer = document.getElementById("recordingTimer");
  const userTranscript = document.getElementById("userTranscript");
  const dobbyResponse = document.getElementById("dobbyResponse");

  function updateUserStatus(speaking) {
    userStatus.textContent = speaking ? "🎙️ Speaking..." : "🎙️ Ready";
    userStatus.classList.toggle("speaking", speaking);
    document
      .querySelector(".user")
      .parentElement.querySelector(".status-indicator")
      .classList.toggle("speaking", speaking);
  }

  function updateDobbyStatus(speaking) {
    dobbyStatus.textContent = speaking ? "🔊 Speaking..." : "🔊 Ready";
    dobbyStatus.classList.toggle("speaking", speaking);
    document
      .querySelector(".dobby")
      .parentElement.querySelector(".status-indicator")
      .classList.toggle("speaking", speaking);
  }

  button.addEventListener("click", () => {
    button.disabled = true;
    updateUserStatus(true);
    socket.emit("start_recording");
  });

  socket.on("timer_update", (data) => {
    timer.textContent = data.seconds;
  });

  socket.on("dobby_response", (data) => {
    button.disabled = false;
    updateUserStatus(false);
    timer.textContent = "";
    userTranscript.textContent = `You said: ${data.user_said}`;
    dobbyResponse.textContent = data.text;
    updateDobbyStatus(true);

    // Reset Dobby's status after speech ends (approximate duration)
    setTimeout(() => {
      updateDobbyStatus(false);
    }, 5000); // Adjust based on typical response length
  });
});
