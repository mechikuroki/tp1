from tkinter import *
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import subprocess, json, os, re, filetype
from pydub import AudioSegment
from pydub.playback import play, _play_with_simpleaudio
from PIL import Image, ImageTk

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Audacity de la Salada")
        self.root.geometry("800x1000")
        self.frame = Frame(self.root, bg="lightblue")
        self.frame.grid(sticky=NSEW, padx=5, pady=5)
        self.style = ttk.Style()
        self.style.theme_use("default")
        for i in range(4): self.frame.grid_columnconfigure(i, weight=1)
        self.frame.grid_rowconfigure(0, weight=5)
        self.frame.grid_rowconfigure(1, weight=5)

        self.play = Button(self.frame, text="Play", command=self.play)
        self.play.grid(row=1, column=0, padx=5, pady=5)
        self.pause = Button(self.frame, text="Pause", command=self.pause)
        self.pause.grid(row=1, column=1, padx=5, pady=5)
        self.next = Button(self.frame, text="Next", command=self.next)
        self.next.grid(row=1, column=2, padx=5, pady=5)
        self.previous = Button(self.frame, text="Previous", command=self.previous)
        self.previous.grid(row=1, column=3, padx=5, pady=5)
        
        self.folder = filedialog.askdirectory(title="Select Folder")
        file_count = len([name for name in os.listdir('.') if os.path.isfile(name)]) 
        if file_count < 50:
            self.musicfiles = []
            self.imagepath = ""
            for i in os.listdir(self.folder):
                if os.path.isfile(os.path.join(self.folder, i)):
                    fileext = filetype.guess(i).lower()
                    if fileext in ["mp3", "wav", "aac", "flac", "ogg", "m4a", "wma", "aiff", "opus", "mka", "ac3"]:
                        self.musicfiles.append(i)
                    elif filext in ["png", "jpg", "gif", "bmp", "webp", "ico"]:
                        self.imagepath = i
        if self.imagepath:
            self.imagepath = Image.open(Path(self.imagepath).resolve())
            self.imagepath = self.imagepath.resize((500, 500), Image.Resampling.LANCZOS)
            self.imagepath = ImageTk.PhotoImage(self.imagepath)
            self.image = Label(self.frame, image=self.imagepath)
            self.image.grid(row=0, column=0, columnspan=4, sticky=NSEW, padx=5, pady=5)
        else:
            messagebox.showerror("Error", "Demasiados archivos en carpeta (deben ser menos de 50")
            self.root.destroy()
        if self.is_ffmpeg_installed() == False:
            messagebox.showerror("Error", "Debe instalar ffmpeg (vea ffmpeg.org)")
            self.root.destroy()
    
    def is_ffmpeg_installed(self):
        try:
            subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    def play(self):
        pass
    def pause(self):
        pass
    def next(self):
        pass
    def previous(self):
        pass
if __name__ == "__main__":
    root = Tk()
    app = MusicPlayer(root)
    root.mainloop()

