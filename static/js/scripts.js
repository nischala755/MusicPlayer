document.addEventListener('DOMContentLoaded', () => {
    // Function to send a request to play a song
    function playSong(song) {
        fetch('/play', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ song: song })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.status);
            // Update the UI to indicate which song is playing
            const nowPlaying = document.getElementById('now-playing');
            nowPlaying.textContent = `Now Playing: ${song}`;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // Add event listeners to all play buttons
    const playButtons = document.querySelectorAll('#playlist button');
    playButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const song = event.target.textContent;
            playSong(song);
        });
    });
});
