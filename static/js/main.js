document.addEventListener('DOMContentLoaded', () => {
    const button = document.getElementById('startDebate');

    button.addEventListener('click', async () => {
        button.disabled = true;
        button.innerHTML = '<span class="button-icon">⏳</span> Starting...';

        try {
            const response = await fetch('/api/start_debate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const data = await response.json();

            if (data.status === 'success') {
                button.innerHTML = '<span class="button-icon">🎤</span> Debate Started!';
                // Future: Initialize WebSocket connection here
            } else {
                throw new Error(data.message || 'Failed to start debate');
            }
        } catch (error) {
            console.error('Error:', error);
            button.innerHTML = '<span class="button-icon">❌</span> Error - Try Again';
        } finally {
            setTimeout(() => {
                button.disabled = false;
                button.innerHTML = '<span class="button-icon">🎯</span> Start Debate!';
            }, 3000);
        }
    });
});
