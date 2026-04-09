from tkinter import *
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from pygame import mixer
from tinytag import TinyTag
from PIL import Image, ImageTk
import os, json
class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Audacity de la Salada")
        self.root.geometry("700x900")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing) 
        self.frame = ttk.Frame(self.root)
        self.frame.grid(sticky=NSEW)
        self.style = ttk.Style()
        self.style.theme_use("clam")
        for i in range(5): self.frame.grid_columnconfigure(i, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=0)

        mixer.init()

        self.playbutton = ttk.Button(self.frame, text="Play", command=self.play)
        self.playbutton.grid(row=2, column=0, padx=5, pady=5)
        self.pausebutton = ttk.Button(self.frame, text="Pause", command=self.pause)
        self.pausebutton.grid(row=2, column=1, padx=5, pady=5)
        self.nextbutton = ttk.Button(self.frame, text="Next", command=self.next)
        self.nextbutton.grid(row=2, column=2, padx=5, pady=5)
        self.previousbutton = ttk.Button(self.frame, text="Previous", command=self.previous)
        self.previousbutton.grid(row=2, column=3, padx=5, pady=5)
        self.stopbutton = ttk.Button(self.frame, text="Stop", command=self.stop)
        self.stopbutton.grid(row=2, column=4, padx=5, pady=5)

        self.image_label = Label(self.frame)
        self.image_label.grid(row=0, column=1, columnspan=3, sticky=NSEW, padx=5, pady=5)
        self.update_cover("default_cover.jpg")

        self.folder = filedialog.askdirectory(title="Select Folder")
        self.lenfolder = 0

        for i in os.listdir(self.folder):
            file = Path(os.path.join(self.folder, i)).resolve()
            if os.path.isfile(file):
                try:
                    mixer.Sound(file)
                except Exception:
                    try:
                        with Image.open(file) as img:
                            img.verify()
                        self.update_cover(file)
                    except (IOError, SyntaxError):
                        continue
                else:
                    metadata = TinyTag.get(file)
                    with open('data.jsonl', 'a') as datafile:
                        datafile.write(json.dumps(metadata.as_dict()) + '\n')
                        self.lenfolder += 1
        self.index = 0

        with open('data.jsonl', 'r') as datafile:
            self.currentsongdata = json.loads(datafile.readline())

        self.set_song_variables()
        self.ismusicpaused = False
        self.play()

    def set_song_variables(self):
        self.currentsongfile = self.currentsongdata["filename"]
        self.currentsongname = self.currentsongdata["title"][0]
        self.currentsongartist = self.currentsongdata["artist"][0]
        self.currentsongalbum = self.currentsongdata["album"][0]
        
    def update_cover(self, path):
        try:
            path = Path(path).resolve()  
            img = Image.open(Path(path).resolve())
            img = img.resize((250, 250), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(img) 
            self.image_label.config(image=self.photo)
        except Exception as e:
            print(f"Could not load image: {e}")
    
    def on_closing(self):
        try:
            os.remove("data.jsonl")
        except Exception:
            pass
        self.root.destroy()

    def play(self):
        if self.ismusicpaused:
            mixer.music.unpause()
            self.ismusicpaused = False
        else:
            mixer.music.unload()
            mixer.music.load(self.currentsongfile)
            mixer.music.play()

    def pause(self):
        mixer.music.pause()
        self.ismusicpaused = True

    def next(self):
        self.index += 1
        if self.index > self.lenfolder:
            self.index = 0
        with open('data.jsonl', 'r') as datafile:
            for index, value in enumerate(datafile):
                if index == self.index:
                    self.currentsongdata = json.loads(value)
                    self.set_song_variables()
                    mixer.music.unload()
                    mixer.music.load(self.currentsongfile)
                    mixer.music.play()
                    break


    def previous(self):
        self.index -= 1
        if self.index < 0:
            self.index = self.lenfolder
        with open('data.jsonl', 'r') as datafile:
            for index, value in enumerate(datafile):
                if index == self.index:
                    self.currentsongdata = json.loads(value)
                    self.set_song_variables()
                    mixer.music.unload()
                    mixer.music.load(self.currentsongfile)
                    mixer.music.play()
                    break
    
    def stop(self):
        mixer.music.stop()
        self.imagepath = Path("default_cover.jpg").resolve()  

if __name__ == "__main__":
    root = Tk()
    app = MusicPlayer(root)
    root.mainloop()

