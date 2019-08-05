from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from tkinter import ttk
from pygame import mixer
import pause
import sys


root = Tk()

status_bar = ttk.Label(root, text="Welcome to Music Player!", relief=SUNKEN, anchor=W)
status_bar.pack(side=BOTTOM, fill=X)


menu_bar = Menu(root)
root.config(menu=menu_bar)

sub_menu = Menu(menu_bar, tearoff=0)

song_list = []


def browse_file():
    global filename
    filename = filedialog.askopenfile()
    add_to_playlist(filename)


def add_to_playlist(f):
    index = 0
    play_list.insert(index, f.name.split("/")[-1])
    song_list.insert(index, f)
    play_list.pack()
    index += 1


sub_menu2 = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=sub_menu)
sub_menu.add_command(label="Open File", command=browse_file)
sub_menu.add_command(label="Exit", command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo(
        "About us", "Copyright @buildwithpython => Youtube.com "
    )


menu_bar.add_cascade(label="About", menu=sub_menu2)
sub_menu2.add_command(label="About us", command=about_us)
mixer.init()
root.title("Music Player!")

left_frame = Frame(root)
left_frame.pack(side=LEFT, padx=15)

right_frame = Frame(root)
right_frame.pack(side=RIGHT)


def play_msc():
    try:
        selected_song = int(play_list.curselection()[0])
        filename = song_list[selected_song]
        if pause.paused:
            mixer.music.unpause()
            pause.paused = False
            status_bar["text"] = "Playing: %s!" % (filename.name.split("/")[-1])
        else:
            stop_msc()            
            mixer.music.load(filename)
            mixer.music.play()
            status_bar["text"] = "Playing: %s!" % (filename.name.split("/")[-1])
    except:
        tkinter.messagebox.showinfo(
            "Error!", "You have to select a file prior to playing it."
        )


def stop_msc():
    mixer.music.stop()
    status_bar["text"] = "Music stopped!"
    pause.paused = False


def pause_msc():
    pause.paused = True
    mixer.music.pause()
    status_bar["text"] = "Music paused!"


def rewind_msc():
    play_msc()


def mute_msc():
    pause.last_volume
    if pause.muted:
        volume_btn.configure(image=volume_photo)
        scale.set(int(pause.last_volume))
        pause.muted = False
    else:
        volume_btn.configure(image=mute_photo)
        pause.last_volume = scale.get()
        scale.set(0)
        pause.muted = True

def delete_song():
    try:
        selected_song = int(play_list.curselection()[0])
        filename = song_list[selected_song]
        play_list.delete(selected_song)
        song_list.remove(filename)        
    except:
        tkinter.messagebox.showinfo(
            "Error!", "You have to select a file prior to deleting it."
        )


top_frame = Frame(right_frame)
top_frame.pack()

middle_frame = Frame(right_frame)
middle_frame.pack(pady=30, padx=30)

bottom_frame = Frame(right_frame)
bottom_frame.pack(pady=10, padx=10)

play_list = Listbox(left_frame)
play_list.pack()

add_button = ttk.Button(left_frame, text="+ Add", command=browse_file)
add_button.pack(side=LEFT, padx=10)

del_button = ttk.Button(left_frame, text="- Del ", command=delete_song)
del_button.pack(side=RIGHT, padx=10)

play_photo = PhotoImage(file="images/play-button.png")
play_btn = ttk.Button(middle_frame, image=play_photo, command=play_msc)
play_btn.grid(row=0, column=0)

stop_photo = PhotoImage(file="images/stop-button.png")
stop_btn = ttk.Button(middle_frame, image=stop_photo, command=stop_msc)
stop_btn.grid(row=0, column=1)

pause_photo = PhotoImage(file="images/pause-button.png")
pause_btn = ttk.Button(middle_frame, image=pause_photo, command=pause_msc)
pause_btn.grid(row=0, column=2)

rewind_photo = PhotoImage(file="images/rewind-button.png")
rewind_btn = ttk.Button(bottom_frame, image=rewind_photo, command=rewind_msc)
rewind_btn.grid(column=0, row=0)

mute_photo = PhotoImage(file="images/mute-button.png")
volume_photo = PhotoImage(file="images/volume-button.png")
volume_btn = ttk.Button(bottom_frame, image=volume_photo, command=mute_msc)
volume_btn.grid(column=1, row=0)


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)


scale = ttk.Scale(bottom_frame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)
mixer.music.set_volume(0.7)
scale.grid(column=2, row=0, padx=15)


root.iconbitmap(r"images/logo.ico")


def on_closing():
    stop_msc()
    root.destroy()


# root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

