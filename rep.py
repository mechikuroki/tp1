from tkinter import *
from tkinter import ttk, messagebox, filedialog, simpledialog
from pathlib import Path
from pygame import mixer
from tinytag import TinyTag
from PIL import Image, ImageTk
import os, json, io, shutil
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

        self.style.configure("Custom.Horizontal.TScale",
                troughcolor="lightblue",   
                background="white")

        self.image_label = Label(self.root, bg="DodgerBlue4", bd=0)
        self.image_label.grid(row=0, column=0, pady=30, padx=20, sticky="nsew")

        self.info_frame = Frame(self.root, bg="DodgerBlue4")
        self.info_frame.grid(row=1, column=0, sticky="ew", padx=30)
        for i in range(2): self.info_frame.columnconfigure(0, weight=1)

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

        mainbtnconfig = [
            ("⏮", self.previous, 0),
            ("⏸", self.play, 1),
            ("▶", self.pause, 2),
            ("⏭", self.next, 3),
            ("⏹", self.stop, 4)
        ]

        for icon, cmd, col in mainbtnconfig:
            btn = ttk.Button(self.controls_frame, text=icon, 
                             command=cmd, style="Player.TButton", width=4)
            btn.grid(row=0, column=col, padx=8, pady=8)

        otherbtnconfig = [
            ("Create", self.make_playlist, 0),
            ("Add" , self.add_to_playlist, 3)
        ]

        for icon, cmd, col in otherbtnconfig:
            btn = ttk.Button(self.controls_frame, text=icon,
                             command=cmd, style="Player.TButton", width=8)
            btn.grid(row=1, column=col, columnspan=2, padx=8, pady=8)

        self.volumebar = ttk.Scale(self.controls_frame, from_=0, to=100, orient=HORIZONTAL, style="Custom.Horizontal.TScale", command=self.volume_changed)
        self.volumebar.grid(row=2, column=0, columnspan=5, sticky=EW, padx=8, pady=8)
        try:
            mixer.init()
        except Exception as e:
            messagebox.showerror("Error", e)
            self.root.destroy()
        self.volumebar.set(100)

        self.audioformattuple = (".wav", ".ogg", ".mp3", ".flac", ".mid", ".midi", ".mod", ".xm", ".it", ".s3m")
        self.audioformatstring = ""
        for i in self.audioformattuple:
            self.audioformatstring += f" *{i}"

        if Path(os.path.join(Path.home(), "My Playlists")).exists() == False:
            os.mkdir(os.path.join(Path.home(), "My Playlists"))
        self.myplaylists = os.path.join(Path.home(), "My Playlists")

        self.get_folder()

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

    def get_folder(self, folder=None):
        with open('data.jsonl', 'w') as datafile:
            datafile.write('')
        
        self.index = 0

        if folder == None:
            try:
                self.folder = filedialog.askdirectory(title="Select Folder")
            except Exception as e:
                print(e)
                messagebox.showerror("Error", e)
                self.root.destroy()
        else:
            try:
                self.folder = folder
            except Exception as e:
                print(e)
                messagebox.showerror("Error", e)
                self.root.destroy()

        self.lenfolder = 0

        for file in os.listdir(self.folder):
            fullpath = os.path.join(self.folder, file)
            if not os.path.isfile(fullpath):
                continue 

            try:
                mixer.music.load(fullpath)
                mixer.music.unload()
                metadata = TinyTag.get(fullpath)
                metadata_dict = {
                        "filename": fullpath, 
                        "title": metadata.title if metadata.title else file,
                        "artist" : metadata.artist if metadata.artist else "Unknown Artist",
                        "album" : metadata.album if metadata.album else "Unknown Album"
                        }
                
                with open('data.jsonl', 'a') as datafile:
                    datafile.write(json.dumps(metadata_dict) + '\n')
                    
                self.lenfolder += 1
                    
            except Exception:
                continue
        if self.lenfolder == 0:
            messagebox.showerror("Error", "No acceptable files in folder")
            self.root.destroy()

        try:
            with open('data.jsonl', 'r') as datafile:
                self.currentsongdata = json.loads(datafile.readline())
        except Exception as e:
            print(e)
            messagebox.showerror("Error", e)
            self.root.destroy()

        self.set_song_variables()
        self.ismusicpaused = False
        self.strict_play()

 
    def make_playlist(self):
        filepaths = filedialog.askopenfilenames(title="Select multiple files", filetypes=[("Music Files", self.audioformatstring)])
        userinput = simpledialog.askstring("Playlist Title", "Please enter your playlist title:")
        try:
            folder = os.path.join(self.myplaylists, userinput)
            os.mkdir(folder)
        except Exception as e:
            messagebox.showerror("Error", e)
        else:
            for file in filepaths:
                dst = os.path.join(folder, Path(file).name)
                shutil.copy2(Path(file), dst)
            self.get_folder(folder=folder)

    
    def add_to_playlist(self):
        filepaths = filedialog.askopenfilenames(title="Select multiple files", filetypes=[("Music Files", self.audioformatstring)])
        for file in filepaths:
            fullpath = os.path.join(self.folder, Path(file).name)
            shutil.copy2(Path(file), fullpath)
            try:
                mixer.music.load(fullpath)
                mixer.music.unload()
                metadata = TinyTag.get(fullpath)
                metadata_dict = {
                        "filename": fullpath, 
                        "title": metadata.title if metadata.title else file,
                        "artist" : metadata.artist if metadata.artist else "Unknown Artist",
                        "album" : metadata.album if metadata.album else "Unknown Album"
                        }
                
                with open('data.jsonl', 'a') as datafile:
                    datafile.write(json.dumps(metadata_dict) + '\n')
                    
                self.lenfolder += 1
                    
            except Exception:
                print(e)
                continue

    def volume_changed(self, value):
        mixer.music.set_volume(float(value)/100)

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
        if self.index > self.lenfolder - 1:
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
            self.index = self.lenfolder - 1

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
        img = img.resize((400, 400), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.photo)
        self.get_folder()
       
if __name__ == "__main__":
    root = Tk()
    app = MusicPlayer(root)
    root.mainloop()

