from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Get list of music files
    music_files = os.listdir('static/music')
    return render_template('index.html', music_files=music_files)

@app.route('/play', methods=['POST'])
def play():
    # Logic to play music
    data = request.json
    song = data['song']
    # Implement logic to play the song
    return jsonify({'status': 'Playing ' + song})

if __name__ == '__main__':
    app.run(debug=True)
