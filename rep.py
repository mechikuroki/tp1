from tkinter import *
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from pygame import mixer
from tinytag import TinyTag
from PIL import Image, ImageTk
import os, json, io
#121212
class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Audacity de la Salada")
        self.root.geometry("500x750")
        self.root.configure(bg="DodgerBlue4") 

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1) 
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=0) 
        self.root.grid_rowconfigure(3, weight=0)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.style.configure("Player.TButton", 
                             font=("Helvetica", 14), 
                             padding=5, 
                             background="#282828", 
                             foreground="white",
                             borderwidth=0)
        self.style.map("Player.TButton", background=[('active', 'lightblue')])

        self.image_label = Label(self.root, bg="DodgerBlue4", bd=0)
        self.image_label.grid(row=0, column=0, pady=30, padx=20, sticky="nsew")

        self.info_frame = Frame(self.root, bg="DodgerBlue4")
        self.info_frame.grid(row=1, column=0, sticky="ew", padx=30)
        self.info_frame.columnconfigure(0, weight=1)

        self.title_label = Label(self.info_frame, text="Song Title", 
                                 font=("Helvetica", 16, "bold"), 
                                 fg="white", bg="DodgerBlue4", anchor="w")
        self.title_label.grid(row=0, column=0, sticky="ew")
        
        self.artist_label = Label(self.info_frame, text="Artist", 
                                  font=("Helvetica", 11), 
                                  fg="#b3b3b3", bg="DodgerBlue4", anchor="w")
        self.artist_label.grid(row=1, column=0, sticky="ew", pady=(2, 15))

        self.progress = ttk.Progressbar(self.root, orient=HORIZONTAL, length=400, mode='determinate')
        self.progress.grid(row=2, column=0, padx=30, pady=10, sticky="ew")

        self.controls_frame = Frame(self.root, bg="DodgerBlue4")
        self.controls_frame.grid(row=3, column=0, pady=(10, 40))

        btn_config = [
            ("⏮", self.previous, 0),
            ("⏸", self.play, 1),
            ("▶", self.pause, 2),
            ("⏭", self.next, 3),
            ("⏹", self.stop, 4)
        ]

        for icon, cmd, col in btn_config:
            btn = ttk.Button(self.controls_frame, text=icon, 
                             command=cmd, style="Player.TButton", width=4)
            btn.grid(row=0, column=col, padx=8)

        mixer.init()

        with open('data.jsonl', 'w') as datafile:
            datafile.write('')
        
        try:
            self.folder = filedialog.askdirectory(title="Select Folder")
        except Exception as e:
            messagebox.showerror("Error", e)
            self.root.destroy

        self.lenfolder = 0

        for file in os.listdir(self.folder):
            full_path = os.path.join(self.folder, file)
            print(full_path)
            if not os.path.isfile(full_path):
                continue 

            try:
                mixer.music.load(full_path)
                mixer.music.unload()
                metadata = TinyTag.get(full_path)
                print(metadata)
                metadata_dict = {
                        "filename": full_path, 
                        "title": metadata.title if metadata.title else file,
                        "artist" : metadata.artist if metadata.artist else "Unknown Artist",
                        "album" : metadata.album if metadata.album else "Unknown Album"
                        }
                print(metadata_dict)
                
                with open('data.jsonl', 'a') as datafile:
                    datafile.write(json.dumps(metadata_dict) + '\n')
                    
                self.lenfolder += 1
                    
            except Exception:
                try:
                    with Image.open(full_path) as img:
                        img.verify()
                    self.update_cover(full_path)
                except Exception:
                    continue

        self.index = 0
        try:
            with open('data.jsonl', 'r') as datafile:
                self.currentsongdata = json.loads(datafile.readline())
        except Exception as e:
            messagebox.showerror("Error", e)
            self.root.destroy

        self.set_song_variables()
        self.ismusicpaused = False
        self.strict_play()

    

    def set_song_variables(self):
        self.currentsongfile = self.currentsongdata["filename"]
        self.currentsongname = self.currentsongdata["title"] if type(self.currentsongdata["title"]) is str else self.currentsongdata["title"][0]
        self.currentsongartist = self.currentsongdata["artist"] if type(self.currentsongdata["artist"]) is str else self.currentsongdata["artist"][0]
        self.currentsongalbum = self.currentsongdata["album"] if type(self.currentsongdata["album"]) is str else self.currentsongdata["album"][0]
        self.title_label.config(text=self.currentsongname)
        self.artist_label.config(text=self.currentsongartist)
        try:
            tag = TinyTag.get(self.currentsongfile, image=True)
            image_data = tag.images.any
            img = Image.open(io.BytesIO(image_data))
        
        except Exception as e:
            img = Image.open("default_cover.jpg")
        
        finally:
                img = img.resize((400, 400), Image.Resampling.LANCZOS)
                self.photo = ImageTk.PhotoImage(img)
                self.image_label.config(image=self.photo)

    def play(self):
        if self.ismusicpaused:
            mixer.music.unpause()
            self.ismusicpaused = False
        else:
            self.strict_play()

    def strict_play(self):
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
                    break
        
        self.set_song_variables()
        self.strict_play()

    def previous(self):
        self.index -= 1
        if self.index < 0:
            self.index = self.lenfolder

        with open('data.jsonl', 'r') as datafile:
            for index, value in enumerate(datafile):
                if index == self.index:
                    self.currentsongdata = json.loads(value)
                    break
        self.set_song_variables()
        self.strict_play()

    def stop(self):
        mixer.music.stop()
        img = Image.open("default_cover.jpg")
        img = img.resize((250, 250), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.photo)

       
if __name__ == "__main__":
    root = Tk()
    app = MusicPlayer(root)
    root.mainloop()

