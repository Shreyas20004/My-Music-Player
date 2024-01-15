import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar
import customtkinter as ctk
from mutagen.mp3 import MP3
import threading
import pygame
import os
import time
# Initialize pygame mixer
pygame.mixer.init()

#Store the current progress
current_pos=0
paused = False
selected_folder_path = ""


def stop_music():
    global paused
    pygame.mixer.music.stop()
    paused = False


def update_progress() :
    global current_pos
    while True:
        if pygame.mixer.music.get_busy() and not paused:
            current_pos=pygame.mixer.music.get_pos()/1000
            progress["value"] = current_pos
            #check if song is over
            if current_pos >= progress["maximum"]:
                stop_music()
                progress["value"]=0

            window.update()
        time.sleep(0.1)



#Create a thread to upgate the progress bar
pt = threading.Thread(target=update_progress)
pt.daemon = True
pt.start()



def selecting_folder():
    global selected_folder_path
    selected_folder_path=filedialog.askdirectory()
    if selected_folder_path:
        lbox.delete(0,tk.END)
        for filename in os.listdir(selected_folder_path):
            if filename.endswith(".mp3"):
                lbox.insert(tk.END,filename)




def previous_song():
    if len(lbox.curselection())>0:
        current_index = lbox.curselection(0,tk.END)
        lbox.selection_set(current_index-1)
        play_selected()
def play():
    global paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        # if music is not paused play the song
        play_selected()
def pause_music():
    global  paused
    pygame.mixer.music.pause()
    paused = True


def play_selected ():
    global current_pos,paused
    if len(lbox.curselection()) > 0:
        current_index = lbox.curselection()[0]
        selected_song = lbox.get(current_index)
        full_path = os.path.join(selected_folder_path,selected_song)
        pygame.mixer.music.load(full_path)
        pygame.mixer.music.play(start=current_pos)
        paused= False
        audio= MP3 (full_path)
        song_duration= audio.info.length
        progress["maximum"]= song_duration



def next_song():
    if len(lbox.curselection())>0:
        current_index=lbox.curselection()[0]
        if current_index< lbox.size()-1:
            lbox.selection_clear(0,tk.END)
            lbox.selection_set(current_index+1)
            play_selected()






# creating main window
window = tk.Tk()
window.title("My music player")
window.geometry("800x700")
window.configure(bg="BLACK")

#creating a label for the music player title
l_music_player = tk.Label(window,text="music player",font=("TKDefaultFont", 30, "bold"))
l_music_player.pack(pady=20)

# Creating a folder to select the music folder
btn_select_folder = ctk.CTkButton(window,text="Select Music Folder",
                                  command=selecting_folder,
                                  font=("TkDefaultFont",18))
btn_select_folder.pack(pady=30)

#creating a list for music
lbox = tk.Listbox(window,width=50,font=("TKDefaultFont",18))
lbox.pack(pady=20)

#creating a frame
btn_frame = tk.Frame(window,bg="BLACK")
btn_frame.pack(pady=30)

#create a button to go to the previos song
btn_previous = ctk.CTkButton(btn_frame,text="<<",command=previous_song,
                            width=50, font=("TKDefaultFont", 18))

btn_previous.pack(side=tk.LEFT,padx=5)

#create a button to play the music
btn_play= ctk.CTkButton(btn_frame,text="Play",command=play,width=50,
                        font=("TKDefaultFont",18))
btn_play.pack(side=tk.LEFT,padx=5)

#create a button to pause the music
btn_pause = ctk.CTkButton(btn_frame,text="Pause",command=pause_music,width=50,
                          font=("TKDefaultFont",18))
btn_pause.pack(side=tk.LEFT,padx=5)

btn_next= ctk.CTkButton(btn_frame,text=">>",command=next_song,width=50,
                        font=("TKDefaultFont",18))
btn_next.pack(side=tk.LEFT,padx=5)

#create a progress bar to indicate the progress of the current song
progress = Progressbar(window,length=300,mode="determinate")
progress.pack(pady=10)
window.mainloop()






