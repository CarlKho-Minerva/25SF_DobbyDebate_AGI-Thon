class DebateArena {
    constructor() {
        this.userVideo = document.getElementById('userVideo');
        this.userTranscript = document.getElementById('userTranscript');
        this.dobbyResponse = document.getElementById('dobbyResponse');
        this.userStatus = document.getElementById('userStatus');
        this.dobbyStatus = document.getElementById('dobbyStatus');
        this.setupVideoStream();
    }

    async setupVideoStream() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            this.userVideo.srcObject = stream;
            this.userStatus.textContent = '🎙️ Ready';
        } catch (error) {
            console.error('Video access error:', error);
            this.userStatus.textContent = '❌ Camera error';
        }
    }

    updateUserTranscript(text) {
        this.userTranscript.textContent = text;
        this.userStatus.textContent = '🗣️ Speaking';
    }

    updateDobbyResponse(text) {
        this.dobbyStatus.textContent = '🗣️ Speaking';
        this.dobbyResponse.textContent = text;
        this.dobbyResponse.classList.add('typing');

        setTimeout(() => {
            this.dobbyResponse.classList.remove('typing');
            this.dobbyStatus.textContent = '🔊 Ready';
        }, 500);
    }

    resetStates() {
        this.userStatus.textContent = '🎙️ Ready';
        this.dobbyStatus.textContent = '🔊 Ready';
        this.userTranscript.textContent = '';
        this.dobbyResponse.textContent = '';
    }
}

export default DebateArena;
