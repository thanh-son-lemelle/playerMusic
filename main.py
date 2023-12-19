import tkinter as tk
import os
from tkinter import *
from tkinter import filedialog, messagebox
from datetime import timedelta
import pygame

#======================================================================
# Variables
#======================================================================
root = tk.Tk()
root.title("Media Player")
root.geometry("800x600")
root.configure(bg="#f0f0f0")
playing_file = False
filepaths = None
pygame.init()
pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
pygame.mixer.music.set_volume(0.5)
duration = 0
progress_percentage = 0
paused = False
current_index = 0
dragging_progressbar = False

#======================================================================#
# Images  
#======================================================================#

img_play = tk.PhotoImage(file="data\\img\\icons8-play-48.png")
img_pause = tk.PhotoImage(file="data\\img\\icons8-pause-48.png")
img_stop = tk.PhotoImage(file="data\\img\\icons8-stop-circled-48.png")
img_rewind = tk.PhotoImage(file="data\\img\\icons8-rewind-button-round-48.png")
img_fastforward = tk.PhotoImage(file="data\\img\\icons8-fast-forward-round-48.png")
img_start = tk.PhotoImage(file="data\\img\\icons8-skip-to-start-48.png")
img_end = tk.PhotoImage(file="data\\img\\icons8-end-48.png")
img_sound = tk.PhotoImage(file="data\\img\\icons8-sound-speaker-48.png")

#======================================================================#
# Fin images  
#======================================================================#
#======================================================================
# Fonctions
#======================================================================
def construction():
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=0)
    root.grid_rowconfigure(2, weight=0)
    root.grid_rowconfigure(3, weight=0)

    root.grid_columnconfigure(0, weight=1, uniform="same_group")
    root.grid_columnconfigure(1, weight=1, uniform="same_group")
    root.grid_columnconfigure(2, weight=1, uniform="same_group")
    root.grid_columnconfigure(3, weight=1, uniform="same_group")
    root.grid_columnconfigure(4, weight=1, uniform="same_group")
    root.grid_columnconfigure(5, weight=1, uniform="same_group")
    root.grid_columnconfigure(6, weight=1, uniform="same_group")
    root.grid_columnconfigure(7, weight=1, uniform="same_group")

def browse_file():
    global filepaths, duration, playing_file, filepath
    filepaths = filedialog.askopenfilenames(initialdir="data\\music", title="Sélectionnez un son", filetypes=[("Audio Files", "*.mp3")])
    for filepath in filepaths:
        title = os.path.basename(filepath)
        title = title.replace(".mp3", "")
        song_list_box.insert(END, title)

def get_duration(filepath):
    global duration
    if filepaths is not None:
        sound = pygame.mixer.Sound(filepath)
        total_duration = int(sound.get_length())
        total_duration_str = str(timedelta(seconds=total_duration))
        time_label.config(text="00:00:00 / " + total_duration_str)
        duration = total_duration
    else:
        time_label.config(text="00:00:00 / 00:00:00")
        duration = 0

def play_file():
    global playing_file, filepaths, duration, paused, filepath
    selected_index = song_list_box.curselection()
    """print(filepaths)
    print (filepath)"""
    
    
    if selected_index:
        selected_file = filepaths[selected_index[0]]
        print ("selected_file",selected_file)
        pygame.mixer.music.load(selected_file)
        pygame.mixer.music.play()
        playing_file = True
        paused = False
        get_duration(selected_file)
        update_media_progress()
        update_current_title(selected_file)
        update_play_buttons()



def pause_file():
    global paused
    global playing_file
    pygame.mixer.music.pause()
    #print("pause")
    paused = True
    print(playing_file)
    update_play_buttons()

def resume_file():
    global playing_file, paused
    pygame.mixer.music.unpause()
    #print("unpause")
    playing_file = True
    paused = False
    update_play_buttons()

def stop_file():
    global playing_file
    pygame.mixer.music.stop()
    playing_file = False
    song_list_box.selection_clear(ACTIVE)

def on_song_select(event):
    global current_index

    # Récupère l'index du titre sélectionné dans la Listbox
    selected_index = song_list_box.curselection()

    # Met à jour current_index si un titre est sélectionné
    if selected_index:
        current_index = selected_index[0]

def next_song():
    global playing_file, current_index, paused

    if filepaths is not None:
        current_index = (current_index + 1) % len(filepaths)
        selected_file = filepaths[current_index]
        pygame.mixer.music.load(selected_file)
        pygame.mixer.music.play()
        playing_file = True
        paused = False
        get_duration(selected_file)
        update_media_progress()
        update_current_title(selected_file)
        update_play_buttons()

def previous_song():
    global playing_file, current_index, paused
    if filepaths is not None:
        current_index = (current_index - 1) % len(filepaths)
        print(current_index,len(filepaths))
        selected_file = filepaths[current_index]
        pygame.mixer.music.load(selected_file)
        pygame.mixer.music.play()
        playing_file = True
        paused = False
        get_duration(selected_file)
        update_media_progress()
        update_current_title(selected_file)
        update_play_buttons()


def toggle_volumeslider():
    if volumeslider.winfo_ismapped():
        volumeslider.grid_forget()
    else:
        volumeslider.grid(row=4, column=7)

def VolAdj(val):
    pygame.mixer.music.set_volume(float(val))

def alert():
    messagebox.showinfo("Alerte", "Bravo!")

def update_play_buttons():
    if paused:
        play_button.grid_forget()
        resume_button.grid(row=4, column=3, padx=5, pady=5)
    else:
        resume_button.grid_forget()
        play_button.grid(row=4, column=3, padx=5, pady=5)

def update_current_title(filepath):
    title = os.path.basename(filepath)
    title = title.replace(".mp3", "")
    current_title_label.config(text=title)

def update_media_progress():
    global progress_percentage, on_click, current_index
    #print ("début fonction")
    #print(playing_file)
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT + 1 and playing_file:  # Événement de fin de lecture
            next_song()

    if playing_file and not dragging_progressbar:
        current_time = pygame.mixer.music.get_pos()
        progress_percentage = ((current_time / 1000) / duration) * 100
        media_progressbar.set(progress_percentage)
        current_time_str = str(timedelta(seconds=current_time // 1000))
        total_duration_str = str(timedelta(seconds=duration))
        time_label.config(text=f"{current_time_str} / {total_duration_str}")
        root.after(1000, update_media_progress)
    else:
        print("pas de lecture suivante")
        media_progressbar.set(0)
        time_label.config(text="00:00:00 / 00:00:00")

def on_click(event):
    global dragging_progress_bar
    if media_progressbar.cget("state") == tk.NORMAL:
        value = (event.x / media_progressbar.winfo_width()) * 100
        media_progressbar.set(value)
        dragging_progress_bar = True
        update_media_position(value)

def update_media_position(new_value):
    global playing_file, duration, dragging_progressbar

    if playing_file and duration > 0:
        new_position = (new_value / 100) * duration * 1000
        pygame.mixer.music.set_pos(new_position)
        current_time_str = str(timedelta(milliseconds=new_position))
        total_duration_str = str(timedelta(seconds=duration))
        time_label.config(text=f"{current_time_str} / {total_duration_str}")
        update_media_progress()
    dragging_progressbar = False


#======================================================================
# Menu bar
#======================================================================
menubar = tk.Menu(root)

menu1 = tk.Menu(menubar, tearoff=0)
menu1.add_command(label="Ouvrir", command=browse_file)
menu1.add_command(label="Éditer", command=alert)
menu1.add_separator()
menu1.add_command(label="Quitter", command=root.quit)
menubar.add_cascade(label="Fichier", menu=menu1)

menu2 = tk.Menu(menubar, tearoff=0)
menu2.add_command(label="Ajouter", command=browse_file)
menu2.add_command(label="Supprimer", command=alert)
menu2.add_command(label="Supprimer la playlist", command=alert)
menubar.add_cascade(label="Playlist", menu=menu2)

menu3 = tk.Menu(menubar, tearoff=0)
menu3.add_command(label="À propos", command=alert)
menubar.add_cascade(label="Aide", menu=menu3)

root.config(menu=menubar)

#======================================================================
# Construction de l'interface
#======================================================================
construction()

song_list_box = tk.Listbox(root, bg="black", fg="green", selectbackground="gray", selectforeground="black")
song_list_box.grid(column=0, row=0, columnspan=8, sticky=tk.NSEW, padx=5, pady=20)
song_list_box.bind('<ButtonRelease-1>', on_song_select)

media_progressbar = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, length=800, showvalue=False)
media_progressbar.grid(column=0, row=1, columnspan=8)
media_progressbar.bind("<B1-Motion>", on_click)

current_title_label = tk.Label(root, text="", font=("Arial", 12, "bold"), fg="#555555", bg="#f0f0f0")
current_title_label.grid(column=0, row=2, columnspan=8, pady=5)

time_label = tk.Label(root, text="00:00:00 / 00:00:00", font=("Arial", 12, "bold"), fg="#555555", bg="#f0f0f0")
time_label.grid(column=3, columnspan=2, row=3, padx=5, pady=5)

# create player control buttons

browse_button = tk.Button(root, text="Parcourir", command=browse_file)
browse_button.grid(row=4, column=0, padx=5, pady=5)

pause_button = tk.Button(root, text="Pause", borderwidth=0, image=img_pause, command=pause_file)
pause_button.grid(row=4, column=2, padx=5, pady=5)


play_button = tk.Button(root, text="Reprendre", borderwidth=0, image=img_play, command=play_file)
play_button.grid(row=4, column=3, padx=5, pady=5)

resume_button = tk.Button(root, text="Reprendre", borderwidth=0, image=img_play, command=resume_file)


back_button = tk.Button(root, image=img_start, borderwidth=0, command=previous_song)
back_button.grid(row=4, column=1)

forward_button = tk.Button(root, image=img_end, borderwidth=0, command=next_song)
forward_button.grid(row=4, column=5)

stop_button = tk.Button(root, text="Arrêter", borderwidth=0, image=img_stop, command=stop_file)
stop_button.grid(row=4, column=4, padx=5, pady=5)

bouton_toggle_scale = tk.Button(root, text="Volume sonore", borderwidth=0, image=img_sound, command=toggle_volumeslider)
bouton_toggle_scale.grid(row=4, column=6, padx=5, pady=5)


volumeslider = tk.Scale(root, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, command=VolAdj)
volumeslider.set(0.5)

update_media_progress()
root.mainloop()
