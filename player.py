import tkinter as tk
from tkinter import filedialog, ttk
from pygame import mixer
import cv2
from PIL import Image, ImageTk
import threading
import time

mixer.init()

root = tk.Tk()
root.title("Music Player")
root.geometry("1000x700")
root.config(bg="#0a0a0a")
root.minsize(700, 550)

current_song = None
paused = False
video_thread = None
playing_video = True
song_length = 0
loop_enabled = False
playlist = []
current_index = -1

VIDEO_PATH = "background.mp4"

canvas = tk.Canvas(root, bg="#0a0a0a", highlightthickness=0)
canvas.place(relx=0, rely=0, relwidth=1, relheight=1)


def play_video():
    global playing_video
    cap = cv2.VideoCapture(VIDEO_PATH)

    while playing_video:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        width = root.winfo_width()
        height = root.winfo_height()

        frame = cv2.resize(frame, (width, height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)

        canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
        canvas.image = imgtk

        time.sleep(0.03)

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
        current_pos = mixer.music.get_pos() / 1000.0

        if song_length > 0:
            progress = (current_pos / song_length) * 100
            progress_bar['value'] = progress
            time_label.config(text=f"{format_time(current_pos)} / {format_time(song_length)}")

        root.after(100, update_progress)
    elif not mixer.music.get_busy() and current_song and not paused:
        if loop_enabled:
            mixer.music.play()
            update_progress()
        else:
            play_next()


def load_songs():
    global playlist
    file_paths = filedialog.askopenfilenames(
        title="Selecciona canciones",
        filetypes=[("Archivos de audio", "*.mp3 *.wav *.ogg")]
    )
    if file_paths:
        playlist.extend(file_paths)
        update_playlist_display()
        playlist_count.config(text=f"📀 {len(playlist)} canciones")


def update_playlist_display():
    playlist_box.delete(0, tk.END)
    for i, song_path in enumerate(playlist):
        song_name = song_path.split('/')[-1]
        display_text = f"{i + 1}. {song_name}"
        playlist_box.insert(tk.END, display_text)

        if i == current_index:
            playlist_box.itemconfig(i, {'bg': '#ff00ff', 'fg': '#000000'})


def play_selected_song(event=None):
    global current_index
    selection = playlist_box.curselection()
    if selection:
        current_index = selection[0]
        load_and_play_song(current_index)


def load_and_play_song(index):
    global current_song, song_length, current_index, paused
    if 0 <= index < len(playlist):
        current_index = index
        current_song = playlist[index]
        song_name = current_song.split('/')[-1]

        if len(song_name) > 40:
            song_name = song_name[:37] + "..."
        song_label.config(text=f"♫ {song_name}")

        mixer.music.load(current_song)
        sound = mixer.Sound(current_song)
        song_length = sound.get_length()

        time_label.config(text=f"00:00 / {format_time(song_length)}")
        progress_bar['value'] = 0

        mixer.music.play()
        paused = False
        update_progress()
        update_playlist_display()


def play_song():
    global paused
    if current_song:
        if paused:
            mixer.music.unpause()
            paused = False
            update_progress()
        else:
            mixer.music.play()
            update_progress()
    elif playlist:
        load_and_play_song(0)
    else:
        song_label.config(text="⚠ Carga canciones primero")


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


def play_next():
    global current_index
    if playlist:
        current_index = (current_index + 1) % len(playlist)
        load_and_play_song(current_index)


def play_prev():
    global current_index
    if playlist:
        current_index = (current_index - 1) % len(playlist)
        load_and_play_song(current_index)


def clear_playlist():
    global playlist, current_index, current_song
    playlist.clear()
    current_index = -1
    current_song = None
    playlist_box.delete(0, tk.END)
    playlist_count.config(text="📀 0 canciones")
    song_label.config(text="No hay canción cargada")
    stop_song()


def toggle_loop():
    global loop_enabled
    loop_enabled = not loop_enabled
    if loop_enabled:
        loop_btn.config(text="🔁 LOOP: ON", bg="#00ff88", fg="#000000")
    else:
        loop_btn.config(text="🔁 LOOP: OFF", bg="#1a1a1a", fg="#666666")


main_container = tk.Frame(root, bg="#0d0d0d", bd=0)
main_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.85, relheight=0.85)

left_frame = tk.Frame(main_container, bg="#0d0d0d")
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

title_label = tk.Label(left_frame, text="RETRO PLAYER",
                       bg="#0d0d0d", fg="#ff00ff",
                       font=("Impact", 24, "bold"))
title_label.pack(pady=10)

subtitle_label = tk.Label(left_frame, text="━━━━━━━━━━━━━━━━",
                          bg="#0d0d0d", fg="#00ffff",
                          font=("Courier", 10))
subtitle_label.pack()

song_label = tk.Label(left_frame, text="No hay canción cargada",
                      bg="#0d0d0d", fg="#00ffff",
                      font=("Courier New", 11, "bold"),
                      wraplength=400)
song_label.pack(pady=10)

time_label = tk.Label(left_frame, text="00:00 / 00:00",
                      bg="#0d0d0d", fg="#00ff88",
                      font=("Digital-7", 14, "bold"))
time_label.pack(pady=5)

style = ttk.Style()
style.theme_use('clam')
style.configure("Neon.Horizontal.TProgressbar",
                background='#ff00ff',
                troughcolor='#1a1a1a',
                bordercolor='#00ffff',
                lightcolor='#ff00ff',
                darkcolor='#ff00ff',
                thickness=18)

progress_bar = ttk.Progressbar(left_frame, style="Neon.Horizontal.TProgressbar",
                               mode='determinate')
progress_bar.pack(fill=tk.X, padx=20, pady=10)

button_frame = tk.Frame(left_frame, bg="#0d0d0d")
button_frame.pack(pady=10)


def get_button_size():
    width = root.winfo_width()
    font_size = max(8, min(14, int(width / 80)))
    btn_width = max(8, min(12, int(width / 100)))
    btn_height = max(1, min(3, int(width / 400)))
    return font_size, btn_width, btn_height


btn_style = {
    "font": ("Impact", 10),
    "bg": "#1a1a1a",
    "activebackground": "#ff00ff",
    "activeforeground": "#000000",
    "bd": 2,
    "relief": tk.RIDGE,
    "cursor": "hand2"
}


def update_button_sizes(event=None):
    font_size, btn_width, btn_height = get_button_size()

    buttons = [btn_load, btn_play, btn_pause, btn_stop, loop_btn, btn_clear]
    for btn in buttons:
        btn.config(font=("Impact", font_size), width=btn_width, height=btn_height)

    btn_prev.config(font=("Impact", font_size), width=int(btn_width * 1.5), height=btn_height)
    btn_next.config(font=("Impact", font_size), width=int(btn_width * 1.5), height=btn_height)


btn_load = tk.Button(button_frame, text="CARGAR", command=load_songs,
                     width=10, height=2, fg="#00ffff", **btn_style)
btn_load.grid(row=0, column=0, padx=4, pady=4)

btn_play = tk.Button(button_frame, text="▶ PLAY", command=play_song,
                     width=10, height=2, fg="#00ff88", **btn_style)
btn_play.grid(row=0, column=1, padx=4, pady=4)

btn_pause = tk.Button(button_frame, text="⏸ PAUSA", command=pause_song,
                      width=10, height=2, fg="#ffff00", **btn_style)
btn_pause.grid(row=0, column=2, padx=4, pady=4)

btn_stop = tk.Button(button_frame, text="⏹ STOP", command=stop_song,
                     width=10, height=2, fg="#ff0055", **btn_style)
btn_stop.grid(row=1, column=0, padx=4, pady=4)

loop_btn = tk.Button(button_frame, text="🔁 LOOP: OFF", command=toggle_loop,
                     width=10, height=2, fg="#666666", **btn_style)
loop_btn.grid(row=1, column=1, padx=4, pady=4)

btn_clear = tk.Button(button_frame, text="🗑 LIMPIAR", command=clear_playlist,
                      width=10, height=2, fg="#ff6600", **btn_style)
btn_clear.grid(row=1, column=2, padx=4, pady=4)

nav_frame = tk.Frame(left_frame, bg="#0d0d0d")
nav_frame.pack(pady=8)

btn_prev = tk.Button(nav_frame, text="⏮ ANTERIOR", command=play_prev,
                     width=15, height=1, fg="#00ffff", **btn_style)
btn_prev.pack(side=tk.LEFT, padx=5)

btn_next = tk.Button(nav_frame, text="SIGUIENTE ⏭", command=play_next,
                     width=15, height=1, fg="#00ffff", **btn_style)
btn_next.pack(side=tk.LEFT, padx=5)

# Footer
footer_label = tk.Label(left_frame, text="Made by Dono Dev",
                        bg="#0d0d0d", fg="#00ffff",
                        font=("Courier New", 8, "bold"))
footer_label.pack(side=tk.BOTTOM, pady=5)

# LADO DERECHO - Playlist
right_frame = tk.Frame(main_container, bg="#0d0d0d", bd=2, relief=tk.RIDGE)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=10, pady=10)

playlist_title = tk.Label(right_frame, text="PLAYLIST",
                          bg="#0d0d0d", fg="#ff00ff",
                          font=("Impact", 14, "bold"))
playlist_title.pack(pady=8)

playlist_count = tk.Label(right_frame, text="📀 0 canciones",
                          bg="#0d0d0d", fg="#00ffff",
                          font=("Courier New", 9))
playlist_count.pack(pady=3)

playlist_frame = tk.Frame(right_frame, bg="#0d0d0d")
playlist_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

scrollbar = tk.Scrollbar(playlist_frame, bg="#1a1a1a")
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

playlist_box = tk.Listbox(playlist_frame,
                          bg="#1a1a1a",
                          fg="#00ffff",
                          font=("Courier New", 9),
                          selectbackground="#ff00ff",
                          selectforeground="#000000",
                          yscrollcommand=scrollbar.set,
                          bd=0,
                          highlightthickness=0,
                          width=30)
playlist_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
playlist_box.bind('<Double-Button-1>', play_selected_song)

scrollbar.config(command=playlist_box.yview)


def blink_title():
    current_color = title_label.cget("fg")
    new_color = "#00ffff" if current_color == "#ff00ff" else "#ff00ff"
    title_label.config(fg=new_color)
    root.after(800, blink_title)


blink_title()

root.bind('<Configure>', update_button_sizes)
update_button_sizes()

try:
    start_video()
except Exception as e:
    print(f"Error al cargar video: {e}")
    canvas.config(bg="#0a0a0a")

root.mainloop()
playing_video = False