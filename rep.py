from tkinter import *
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from pygame import mixer
from tinytag import TinyTag
from PIL import Image, ImageTk

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Audacity de la Salada")
        self.root.geometry("800x1000")
        self.frame = ttk.Frame(self.root)
        self.frame.grid(sticky=NSEW, padx=5, pady=5)
        self.style = ttk.Style()
        self.style.theme_use("clam")
        for i in range(4): self.frame.grid_columnconfigure(i, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=0)

        mixer.init()

        self.play = ttk.Button(self.frame, text="Play", command=self.play)
        self.play.grid(row=2, column=0, padx=5, pady=5)
        self.pause = ttk.Button(self.frame, text="Pause", command=self.pause)
        self.pause.grid(row=2, column=1, padx=5, pady=5)
        self.next = ttk.Button(self.frame, text="Next", command=self.next)
        self.next.grid(row=2, column=2, padx=5, pady=5)
        self.previous = ttk.Button(self.frame, text="Previous", command=self.previous)
        self.previous.grid(row=2, column=3, padx=5, pady=5)
        self.stop = ttk.Button(self.frame, text="Stop", command=self.stop)
        self.stop.grid(row=2, column=4, padx=5, pady=5)

        self.imagepath = Path("default_cover.jpg").resolve()  
        self.image_label = Label(self.frame, bg="lightblue")
        self.image_label.grid(row=0, column=0, columnspan=5, sticky=NSEW, padx=5, pady=5)
        self.update_cover(self.imagepath)

        self.folder = filedialog.askdirectory(title="Select Folder")
        for i in os.listdir(self.folder):
            if os.path.isfile(os.path.join(self.folder, i)):
                file = Path(os.path.join(self.folder, i)).resolve()
                try:
                    mixer.Sound(file)
                except Exception:
                    continue
                else:
                    metadata = TinyTag.get(file)
                    with open('data.jsonl', 'a') as datafile:
                        datafile.write(json.dumps(metadata.as_dict()) + '\n')
                    
                
    def update_cover(self, path):
        try:
            img = Image.open(Path(path).resolve())
            img = img.resize((500, 500), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(img) 
            self.image_label.config(image=self.photo)
        except Exception as e:
            print(f"Could not load image: {e}")

    def play(self):
        pass
    def pause(self):
        pass
    def next(self):
        pass
    def previous(self):
        pass
    def stop(self):
        pass

if __name__ == "__main__":
    root = Tk()
    app = MusicPlayer(root)
    root.mainloop()

