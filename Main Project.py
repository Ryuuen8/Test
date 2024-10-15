from tkinter import *
from tkinter import ttk, filedialog
import os
import pygame

class IntroWindow:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#56a1cc")
        self.root.title("EyeEase")
        self.root.geometry("640x480")

        self.frame = Frame(root, bg="#56a1cc")
        self.frame.place(relx=0.5, rely=0.5, anchor="s")

        self.main_label = Label(self.frame, text="Welcome to EyeEase", font=("Helvetica", 24), bg="#56a1cc")
        self.main_label.grid(row=0, column=0, pady=20)

        self.next_button = Button(self.frame, text="Proceed", command=self.intro, bg="#FFB3C1", borderwidth=0)
        self.next_button.grid(row=1, column=0, pady=20)
        self.style_button(self.next_button)

    def style_button(self, button):
        button.config(
            relief="flat",
            bg="#FFB3C1"
        )
        button.bind("<Enter>", lambda e: button.config(bg="#FF9AAB"))
        button.bind("<Leave>", lambda e: button.config(bg="#FFB3C1")) 

    def intro(self):
        paragraph_text = (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        )

        self.intro_label = Label(self.root, text=paragraph_text, wraplength=350, justify="left", bg="#56a1cc")
        self.intro_label.grid(pady=20)

        self.hide_widgets([self.main_label, self.next_button])

        self.main_button_frame1 = Frame(self.root, bg="#56a1cc")
        self.main_button_frame1.grid(pady=10)

        self.next_button1 = Button(self.main_button_frame1, text="Proceed", command=self.next_window, bg="#FFB3C1", borderwidth=0)
        self.next_button1.grid(padx=5)
        self.style_button(self.next_button1)

    def hide_widgets(self, widgets):
        for widget in widgets:
            widget.pack_forget()
            widget.grid_forget()

    def next_window(self):
        timer_window = TimerWindow(self.root)
        self.hide_widgets([self.intro_label, self.main_button_frame1])

class TimerWindow:
    def __init__(self, root):
        self.root = root
        pygame.init()

        self.timer_label_frame = Frame(root, bg="#56a1cc")
        self.timer_label_frame.place(relx=0.5, rely=0.2, anchor="e")

        self.time_label = Label(self.timer_label_frame, text="ARE YOU READY?", font=("Helvetica", 24), bg="#56a1cc")
        self.time_label.grid(row=1, column=0, pady=20)

        self.button_label_frame = Frame(root, bg="#56a1cc")
        self.button_label_frame.place(relx=0.1, rely=0.3, anchor="e")

        self.start_button = Button(self.button_label_frame, text="Start", command=self.start_timer, bg="#FFB3C1", borderwidth=0)
        self.start_button.grid(row=2, column=0, pady=10)
        self.style_button(self.start_button)

        self.reset_button = Button(root, text="Reset", command=self.reset_timer, bg="#FFB3C1", borderwidth=0)
        self.reset_button.place(relx=0.5, rely=0.3, anchor="e")
        self.style_button(self.reset_button)

        self.current_label = Label(root, text="Ringtone: ", bg="#56a1cc", font=("Helvetica", 12))
        self.current_label.place(relx=0.2, rely=0.6, anchor="e")

        self.songs = self.load_songs() 
        self.current_song = None

     
        self.current_combobox = ttk.Combobox(root, values=[os.path.splitext(os.path.basename(song))[0] for song in self.songs])
        if self.songs:
            self.current_combobox.current(0)
        self.current_combobox.place(relx=0.42, rely=0.6, anchor="e")

        self.play_button = Button(root, text="Play", command=self.play, bg="#FFB3C1", borderwidth=0)
        self.play_button.place(relx=0.5, rely=0.7, anchor="e")
        self.style_button(self.play_button)

        self.select_button = Button(root, text="Select Song", command=self.select_song, bg="#FFB3C1", borderwidth=0)
        self.select_button.place(relx=0.3, rely=0.7, anchor="e")
        self.style_button(self.select_button)

        self.running = False
        self.elapsed_time = 10

    def style_button(self, button):
        """Styles the button with padding and hover effects."""
        button.config(
            relief="flat",
            bg="#FFB3C1"
        )
        button.bind("<Enter>", lambda e: button.config(bg="#FF9AAB"))  
        button.bind("<Leave>", lambda e: button.config(bg="#FFB3C1"))  

    def load_songs(self):
        """Load song paths from a text file."""
        try:
            with open("songs.txt", "r", encoding="utf-8") as file: 
                songs = file.read().splitlines()  
                return songs
        except FileNotFoundError:
            return [] 

    def save_song(self, song_path):
        """Append a new song path to the text file."""
        with open("songs.txt", "a", encoding="utf-8") as file:
            file.write(song_path + "\n")
    def play(self):
        selected_index = self.current_combobox.current()
        if selected_index >= 0:
            self.current_song = self.songs[selected_index]
        
            if self.current_song:
                print(f"Loading song: {self.current_song}")
                if os.path.exists(self.current_song):
                    pygame.mixer.music.load(self.current_song)
                    pygame.mixer.music.play()
                else:
                    print(f"File not found: {self.current_song}")
            else:
                print("No song selected.")

    def update_timer(self):
        if self.running and self.elapsed_time > 0:
            self.elapsed_time -= 1
            self.time_label.config(text=self.format_time(self.elapsed_time))
            self.time_label.place(relx=0.7, rely=0.5, anchor="e")
            self.root.after(1000, self.update_timer)
        elif self.elapsed_time <= 0:
            self.time_label.config(text="Time's Up")
            self.time_label.place(relx=0.7, rely=0.5, anchor="e")
            self.running = False
            if self.current_song:
                print(f"Loading song: {self.current_song}")
                if os.path.exists(self.current_song):
                    pygame.mixer.music.load(self.current_song)
                    pygame.mixer.music.play()
                else:
                    print(f"File not found: {self.current_song}")

    def start_timer(self):
        if not self.running:
            self.running = True
            self.update_timer()

    def reset_timer(self):
        self.running = False
        self.elapsed_time = 10
        self.time_label.config(text="Time: 00:00:10")
        self.time_label.place(relx=0.9, rely=0.5, anchor="e")
        pygame.mixer.music.stop()

    def format_time(self, elapsed_time):
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    
    def select_song(self):
        song_path = filedialog.askopenfilename(title="Select a Song", filetypes=(("MP3 Files", "*.mp3"), ("All Files", "*.*")))
        if song_path:
            song_name = os.path.basename(song_path)
            self.songs.append(song_path)
            self.current_combobox['values'] = [os.path.splitext(os.path.basename(song))[0] for song in self.songs]
            self.current_combobox.current(len(self.songs) - 1)
            self.save_song(song_path)

if __name__ == "__main__":
    root = Tk()
    timer_app = IntroWindow(root)
    root.mainloop()
