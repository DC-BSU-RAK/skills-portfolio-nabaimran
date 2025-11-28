import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

root = tk.Tk()
root.geometry("1280x720")
root.resizable(False, False)

# ---------- FUNCTION TO PLAY ANIMATED GIF ----------
def play_gif(canvas, gif_path):
    gif = Image.open(gif_path)
    frames = [ImageTk.PhotoImage(img.copy().resize((1280,720))) for img in ImageSequence.Iterator(gif)]

    def update(ind):
        frame = frames[ind]
        canvas.create_image(0, 0, image=frame, anchor="nw")
        canvas.image = frame
        root.after(40, update, (ind+1) % len(frames))  # 40ms = ~25fps

    update(0)

# ---------- SHOW GIF ----------
def show_gif(path):
    canvas = tk.Canvas(root, width=1280, height=720, highlightthickness=0)
    canvas.pack()
    play_gif(canvas, path)

    # TEMP — to read clicks
    def coords(event):
        print(event.x, event.y)
    canvas.bind("<Button-1>", coords)

show_gif("Assessment 1 - Skills Portfolio\\home.gif")

root.mainloop()
