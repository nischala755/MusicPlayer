import tkinter as tk
from tkinter import ttk
import pygame
import os
from mutagen.mp3 import MP3
import random

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# Create a playlist (list of audio file paths)
playlist = [
    "C:/Users/nisch/Downloads/New Hero in Town.mp3",
    "C:/Users/nisch/Downloads/Morning.mp3",
    "C:/Users/nisch/Downloads/New Hero in Town.mp3"
]

# Index to keep track of the current song in the playlist
current_song_index = 0

# Flag to indicate shuffle mode
shuffle_mode = False

# Flag to indicate repeat mode
repeat_mode = False

def load_and_play_song(index):
    global current_song_index
    # Stop any currently playing song
    pygame.mixer.music.stop()
    # Load the selected song from the playlist
    pygame.mixer.music.load(playlist[index])
    # Play the loaded song
    pygame.mixer.music.play()
    # Update the song info label
    update_song_info_label(playlist[index])
    # Update the current song index
    current_song_index = index

def play_song():
    pygame.mixer.music.unpause()

def pause_song():
    pygame.mixer.music.pause()

def stop_song():
    pygame.mixer.music.stop()

def skip_forward():
    global current_song_index, shuffle_mode
    if repeat_mode:
        load_and_play_song(current_song_index)
    else:
        if shuffle_mode:
            current_song_index = random.randint(0, len(playlist) - 1)
        else:
            current_song_index = (current_song_index + 1) % len(playlist)
        load_and_play_song(current_song_index)

def skip_backward():
    global current_song_index, shuffle_mode
    if repeat_mode:
        load_and_play_song(current_song_index)
    else:
        if shuffle_mode:
            current_song_index = random.randint(0, len(playlist) - 1)
        else:
            current_song_index = (current_song_index - 1) % len(playlist)
        load_and_play_song(current_song_index)

def toggle_shuffle():
    global shuffle_mode
    shuffle_mode = not shuffle_mode

def toggle_repeat():
    global repeat_mode
    repeat_mode = not repeat_mode
    update_buttons_state()

def set_volume(volume):
    # Convert volume to float and scale from 0-100 to 0.0-1.0
    pygame.mixer.music.set_volume(float(volume) / 100)

def update_song_info_label(file_path):
    audio = MP3(file_path)
    title = audio["TIT2"].text[0] if "TIT2" in audio else "Unknown Title"
    artist = audio["TPE1"].text[0] if "TPE1" in audio else "Unknown Artist"
    song_info_label.config(text=f"Now Playing: {title} - {artist}")

def load_selected_song(event):
    selection_index = playlist_listbox.curselection()
    if selection_index:
        load_and_play_song(selection_index[0])

def update_buttons_state():
    shuffle_button.config(state=tk.NORMAL if not repeat_mode else tk.DISABLED)
    repeat_button.config(state=tk.NORMAL if not shuffle_mode else tk.DISABLED)

# Set up the Tkinter root window
root = tk.Tk()
root.title("Music Player")

# Create a frame for holding the controls
controls_frame = ttk.Frame(root)
controls_frame.pack(pady=10)

# Create buttons for playback control
play_button = ttk.Button(controls_frame, text="Play", command=play_song)
pause_button = ttk.Button(controls_frame, text="Pause", command=pause_song)
stop_button = ttk.Button(controls_frame, text="Stop", command=stop_song)
skip_forward_button = ttk.Button(controls_frame, text="Skip Forward", command=skip_forward)
skip_backward_button = ttk.Button(controls_frame, text="Skip Backward", command=skip_backward)
shuffle_button = ttk.Button(controls_frame, text="Shuffle", command=toggle_shuffle)
repeat_button = ttk.Button(controls_frame, text="Repeat", command=toggle_repeat)

# Arrange the buttons using grid layout
play_button.grid(row=0, column=0, padx=5)
pause_button.grid(row=0, column=1, padx=5)
stop_button.grid(row=0, column=2, padx=5)
skip_backward_button.grid(row=0, column=3, padx=5)
skip_forward_button.grid(row=0, column=4, padx=5)
shuffle_button.grid(row=0, column=5, padx=5)
repeat_button.grid(row=0, column=6, padx=5)

# Create a volume control slider
volume_label = ttk.Label(controls_frame, text="Volume:")
volume_slider = ttk.Scale(controls_frame, from_=0, to=100, orient="horizontal", command=set_volume)

# Arrange the volume slider using grid layout
volume_label.grid(row=1, column=0, padx=5, pady=5)
volume_slider.grid(row=1, column=1, columnspan=4, padx=5, pady=5)

# Create labels for displaying current playback time and song duration
current_time_label = ttk.Label(controls_frame, text="00:00")
total_time_label = ttk.Label(controls_frame, text="00:00")

# Arrange the time labels using grid layout
current_time_label.grid(row=1, column=5, padx=5)
total_time_label.grid(row=1, column=6, padx=5)

# Function to update the current playback time label
def update_current_time_label():
    current_time = pygame.mixer.music.get_pos() / 1000
    minutes = int(current_time // 60)
    seconds = int(current_time % 60)
    current_time_label.config(text=f"{minutes:02d}:{seconds:02d}")

# Function to update the total duration label of the song
def update_total_time_label(file_path):
    audio = MP3(file_path)
    total_time = audio.info.length
    minutes = int(total_time // 60)
    seconds = int(total_time % 60)
    total_time_label.config(text=f"{minutes:02d}:{seconds:02d}")

# Function to update both time labels
def update_time_labels():
    update_current_time_label()
    update_total_time_label(playlist[current_song_index])
    root.after(1000, update_time_labels)

# Create the song info label
song_info_label = ttk.Label(root, text="Now Playing: ", font=("Helvetica", 14))
song_info_label.pack(pady=10)

# Create the playlist listbox
playlist_frame = ttk.Frame(root)
playlist_frame.pack(pady=10)
playlist_listbox = tk.Listbox(playlist_frame, height=10, width=50, selectmode=tk.SINGLE)
playlist_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
scrollbar = ttk.Scrollbar(playlist_frame, orient=tk.VERTICAL, command=playlist_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
playlist_listbox.config(yscrollcommand=scrollbar.set)

# Add songs to the playlist listbox
for song in playlist:
    playlist_listbox.insert(tk.END, os.path.basename(song))

# Bind the listbox selection event to load the selected song
playlist_listbox.bind("<<ListboxSelect>>", load_selected_song)

# Start updating the time labels
update_time_labels()

# Run the Tkinter event loop
root.mainloop()
