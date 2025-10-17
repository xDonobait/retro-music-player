import tkinter as tk
from tkinter import filedialog
from pygame import mixer
import cv2
from PIL import Image, ImageTk
import threading
import time

mixer.init()

root = tk.Tk()
root.title("Retro Music Player")
root.geometry("800x600")
root.config(bg="#000000")

current_song = None
paused = False
video_thread = None
playing_video = True
song_length = 0

VIDEO_PATH = "background.mp4"

# Canvas para el video de fondo
canvas = tk.Canvas(root, width=800, height=600, bg="#000000", highlightthickness=0)
canvas.place(x=0, y=0)


def play_video():
    global playing_video

    cap = cv2.VideoCapture(VIDEO_PATH)

    while playing_video:
        ret, frame = cap.read()

        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        frame = cv2.resize(frame, (800, 600))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)

        canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
        canvas.image = imgtk

        time.sleep(0.03)  # ~30 FPS

    cap.release()


def start_video():
    global video_thread, playing_video
    playing_video = True
    video_thread = threading.Thread(target=play_video, daemon=True)
    video_thread.start()


def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"


def update_progress():
    if mixer.music.get_busy() and not paused:
        current_pos = mixer.music.get_pos() / 1000.0  # Convertir a segundos

        if song_length > 0:
            progress = (current_pos / song_length) * 100
            progress_bar['value'] = progress
            time_label.config(text=f"{format_time(current_pos)} / {format_time(song_length)}")

        root.after(100, update_progress)
    elif not mixer.music.get_busy() and current_song and not paused:
        progress_bar['value'] = 0
        time_label.config(text="00:00 / 00:00")


def load_song():
    global current_song, song_length
    file_path = filedialog.askopenfilename(
        title="Selecciona una canción",
        filetypes=[("Archivos de audio", "*.mp3 *.wav *.ogg")]
    )
    if file_path:
        current_song = file_path
        song_name = file_path.split('/')[-1]
        song_label.config(text=f"🎵 {song_name}")

        mixer.music.load(current_song)
        sound = mixer.Sound(current_song)
        song_length = sound.get_length()

        time_label.config(text=f"00:00 / {format_time(song_length)}")
        progress_bar['value'] = 0


def play_song():
    global paused
    if current_song:
        if paused:
            mixer.music.unpause()
            paused = False
        else:
            mixer.music.play()
        update_progress()
    else:
        song_label.config(text="⚠️ Carga una canción primero")


def pause_song():
    global paused
    mixer.music.pause()
    paused = True


def stop_song():
    global paused
    mixer.music.stop()
    paused = False
    progress_bar['value'] = 0
    if song_length > 0:
        time_label.config(text=f"00:00 / {format_time(song_length)}")


control_frame = tk.Frame(root, bg="#1a1a1a", bd=0)
control_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=600, height=400)

title_label = tk.Label(control_frame, text="MUSIC PLAYER RETRO",
                       bg="#1a1a1a", fg="#ff4c4c", font=("Arial Black", 20, "bold"))
title_label.pack(pady=20)

song_label = tk.Label(control_frame, text="Ninguna canción cargada",
                      bg="#1a1a1a", fg="#ffffff", font=("Arial", 14))
song_label.pack(pady=10)

time_label = tk.Label(control_frame, text="00:00 / 00:00",
                      bg="#1a1a1a", fg="#00ff00", font=("Courier", 12, "bold"))
time_label.pack(pady=5)

from tkinter import ttk

style = ttk.Style()
style.theme_use('clam')
style.configure("custom.Horizontal.TProgressbar",
                background='#ff4c4c',
                troughcolor='#333333',
                bordercolor='#000000',
                lightcolor='#ff4c4c',
                darkcolor='#ff4c4c')

progress_bar = ttk.Progressbar(control_frame, style="custom.Horizontal.TProgressbar",
                               length=500, mode='determinate')
progress_bar.pack(pady=10)

button_frame = tk.Frame(control_frame, bg="#1a1a1a")
button_frame.pack(pady=20)

btn_style = {
    "width": 12,
    "height": 2,
    "font": ("Arial", 10, "bold"),
    "bg": "#ff4c4c",
    "fg": "white",
    "activebackground": "#ff6b6b",
    "bd": 3,
    "relief": tk.RAISED
}

btn_load = tk.Button(button_frame, text="CARGAR", command=load_song, **btn_style)
btn_load.grid(row=0, column=0, padx=5, pady=5)

btn_play = tk.Button(button_frame, text="▶PLAY", command=play_song, **btn_style)
btn_play.grid(row=0, column=1, padx=5, pady=5)

btn_pause = tk.Button(button_frame, text="⏸PAUSA", command=pause_song, **btn_style)
btn_pause.grid(row=1, column=0, padx=5, pady=5)

btn_stop = tk.Button(button_frame, text="⏹STOP", command=stop_song, **btn_style)
btn_stop.grid(row=1, column=1, padx=5, pady=5)

footer_label = tk.Label(control_frame, text="Made with 🔥 by Dono",
                        bg="#1a1a1a", fg="#666666", font=("Arial", 9))
footer_label.pack(side=tk.BOTTOM, pady=10)

try:
    start_video()
except Exception as e:
    print(f"Error al cargar video: {e}")
    canvas.config(bg="#1a1a1a")  #fallback background color

root.mainloop()

playing_video = False