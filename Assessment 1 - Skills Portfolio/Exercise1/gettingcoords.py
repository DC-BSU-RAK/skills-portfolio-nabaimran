import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

root = tk.Tk()
root.geometry("1280x720")
root.resizable(False, False)

def show_gif(path):
    for widget in root.winfo_children():
        widget.destroy()

    canvas = tk.Canvas(root, width=1280, height=720, highlightthickness=0)
    canvas.pack()

    img = Image.open(path)

    frames = []
    if getattr(img, "is_animated", False):
        # Extract GIF frames
        for frame in ImageSequence.Iterator(img):
            frame = frame.resize((1280, 720))
            frames.append(ImageTk.PhotoImage(frame))
    else:
        frames.append(ImageTk.PhotoImage(img.resize((1280, 720))))

    canvas.frames = frames
    canvas.frame_index = 0

    def animate():
        canvas.delete("all")
        canvas.create_image(0, 0, anchor="nw", image=canvas.frames[canvas.frame_index])
        canvas.frame_index = (canvas.frame_index + 1) % len(canvas.frames)
        if len(frames) > 1:  # Only animate if more than 1 frame
            root.after(50, animate)

    animate()
    return canvas

canvas = show_gif(r"Assessment 1 - Skills Portfolio\Exercise1\scoreboard2.png")

def coords(event):
    print(event.x, event.y)

canvas.bind("<Button-1>", coords)

root.mainloop()
