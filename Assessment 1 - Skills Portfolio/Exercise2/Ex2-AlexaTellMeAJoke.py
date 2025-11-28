# Alexa Joke Teller Application
# This application uses Tkinter to create a GUI that tells jokes.
# Jokes are read from a text file named randomJokes.txt.    
# ChatGPT was used to help and then i designed the bg image and modified the code to improve the GUI appearance.


import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os


# defining the main application class
class AlexaJokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa - Joke Assistant")
        self.root.geometry("700x400")

        self.center_window(700, 400)
        self.jokes = self.load_jokes()

        self.current_setup = ""
        self.current_punchline = ""

        self.title_font = ("Comic Sans MS", 22, "bold")
        self.setup_font = ("Comic Sans MS", 16, "bold")
        self.punchline_font = ("Comic Sans MS", 15, "italic")
        self.button_font = ("Comic Sans MS", 12, "bold")

        self.accent_color = "#00A8E8"
        self.text_color = "#FFFFFF"

        self.create_background()
        self.create_widgets()
 
# center the window on the screen
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))   
        y = int((screen_height / 2) - (height / 2))
        self.root.geometry(f"{width}x{height}+{x}+{y}")


# load jokes from the text file
    def load_jokes(self):
        jokes = []
        file_path = r"Assessment 1 - Skills Portfolio\Exercise2\randomJokes.txt"

        if not os.path.exists(file_path):
            messagebox.showerror("File Error", f"Could not find {file_path}.")
            return jokes
# read jokes from file
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    if "?" in line:
                        q_index = line.find("?")
                        setup = line[:q_index + 1].strip()
                        punchline = line[q_index + 1:].strip()
                        if setup and punchline:
                            jokes.append((setup, punchline))
        except Exception as e:
            messagebox.showerror("Error", f"Error reading jokes: {e}")

        if not jokes:
            messagebox.showwarning("No Jokes", "No valid jokes found in the file.")
        return jokes


# create background image or color
# here o set a background image if available, otherwise a solid color
# i designed a background image named joketkinter2.png and placed it in the same folder as the code file 
    def create_background(self):
        bg_path = r"Assessment 1 - Skills Portfolio\Exercise2\joketkinter2.png"

        if os.path.exists(bg_path):
            image = Image.open(bg_path)
            image = image.resize((700, 400), Image.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(image)
            self.bg_label = tk.Label(self.root, image=self.bg_image, border=0, highlightthickness=0)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            self.root.config(bg="#101820")
 

 # creating  the main widgets
    def create_widgets(self):
        self.title_label = tk.Label(
            self.root,
            text="Alexa, tell me a Joke",
            font=self.title_font,
            fg=self.accent_color,
            bg="#000000",
        )
        self.title_label.pack(pady=15)

        # Transparent frame
        self.joke_frame = tk.Frame(self.root, bg="#000000", highlightthickness=0, border=0)
        self.joke_frame.pack(pady=10, fill="both", expand=True)

        # Labels now have transparent matching bg
        self.setup_label = tk.Label(
            self.joke_frame,
            text="Click the button below to hear a joke!",
            font=self.setup_font,
            fg=self.text_color,
            bg="#000000",   # removed white
            wraplength=650,
            justify="center",
        )
        self.setup_label.pack(pady=10)

        self.punchline_label = tk.Label(
            self.joke_frame,
            text="",
            font=self.punchline_font,
            fg="#FFD447",
            bg="#000000",   # removed white
            wraplength=650,
            justify="center",
        )
        self.punchline_label.pack(pady=10)

        # Transparent button frame
        self.button_frame = tk.Frame(self.root, bg="#000000", highlightthickness=0, border=0)
        self.button_frame.pack(pady=5)

        self.joke_button = tk.Button(
            self.button_frame,
            text="Alexa tell me a Joke",
            font=self.button_font,
            bg="#1B263B",
            fg=self.text_color,
            width=20,
            command=self.show_new_joke,
            border=0,
            highlightthickness=0
        )
        self.joke_button.grid(row=0, column=0, padx=10, pady=5)
        # punchline button
        self.punchline_button = tk.Button(
            self.button_frame,
            text="Show Punchline",
            font=self.button_font,
            bg="#1B263B",
            fg=self.text_color,
            width=15,
            command=self.show_punchline,
            state="disabled",
            border=0,
            highlightthickness=0
        )
        self.punchline_button.grid(row=0, column=1, padx=10, pady=5)
            # next joke button
        self.next_button = tk.Button(
            self.button_frame,
            text="Next Joke",
            font=self.button_font,
            bg="#1B263B",
            fg=self.text_color,
            width=12,
            command=self.show_new_joke,
            state="disabled",
            border=0,
            highlightthickness=0
        )
        self.next_button.grid(row=0, column=2, padx=10, pady=5)
        # quit button
        self.quit_button = tk.Button(
            self.root,
            text="Quit",
            font=self.button_font,
            bg="#8B0000",
            fg="white",
            width=10,
            command=self.root.quit,
            border=0,
            highlightthickness=0
        )
        self.quit_button.pack(pady=5)

        # Removed white footer bg
        self.footer = tk.Label(
            self.root,
            text='Tip: Click "Alexa tell me a Joke" to start, then "Show Punchline".',
            font=("Comic Sans MS", 10),
            fg="#DDDDDD",
            bg="#000000"  # make footer blend in
        )
        self.footer.pack(side="bottom", pady=5)
# show a new joke
    def show_new_joke(self):
        if not self.jokes:
            self.setup_label.config(text="No jokes available. Check your randomJokes.txt file.")
            return
        # select a random joke
        self.current_setup, self.current_punchline = random.choice(self.jokes)
        self.setup_label.config(text=self.current_setup)
        self.punchline_label.config(text="")
        self.punchline_button.config(state="normal")
        self.next_button.config(state="normal")

    def show_punchline(self):
        self.punchline_label.config(text=self.current_punchline)

# main program execution
if __name__ == "__main__":
    root = tk.Tk()
    app = AlexaJokeApp(root)
    root.mainloop()
