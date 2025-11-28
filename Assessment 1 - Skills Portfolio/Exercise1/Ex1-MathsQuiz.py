# Arcade Maths Quiz Application
# This program creates an interactive maths quiz with multiple screens using tkinter.
# It includes an animated home screen, instructions, difficulty selection, quiz questions,
# and a scoreboard displaying the final score and grade.    
# With the help of ChatGPT (specifically used for getting coordinates of hotspots)

import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import random

# file paths 
# to make it easier to change later if needed
home_gif = r"Assessment 1 - Skills Portfolio\Exercise1\home.gif"
difficulty_img = r"Assessment 1 - Skills Portfolio\Exercise1\difficulty.png"
instructions_img = r"Assessment 1 - Skills Portfolio\Exercise1\instructions.png"
quiz_bg_img = r"Assessment 1 - Skills Portfolio\Exercise1\quiz_bg.png"
scoreboard_img = r"Assessment 1 - Skills Portfolio\Exercise1\scoreboard2.png"

# hotspot rectangles (x1, y1, x2, y2) 
# coordinates for clickable areas on each screen
# i coded a simple function to detect clicks within these areas which you can find in "gettingcoords.py"

home_rects = {
    "play":    (553, 301, 720, 333),
    "instr":   (562, 362, 722, 396),
    "quit":    (553, 426, 711, 459),
}
instructions_rects = {"back": (551, 661, 733, 694)}
difficulty_rects = {
    "easy":     (254, 328, 473, 435),
    "moderate": (528, 339, 736, 439),
    "advanced": (800, 347, 1002, 436),
    "back":     (550, 500, 728, 527)
}

# global variables 
# these will be used and modified throughout the program
score = 0
question_num = 0
attempt = 1
level = ""
num1 = num2 = answer = 0
scoreboard_widgets = []   
# to keep track of widgets on the scoreboard screen for cleanup
root = tk.Tk()
root.geometry("1280x720")
root.title("Arcade Maths Quiz")
root.resizable(False, False)
canvas = tk.Canvas(root, width=1280, height=720, highlightthickness=0)
canvas.place(x=0, y=0)
current_hotspots = []
home_label = tk.Label(root, bd=0, highlightthickness=0)
home_label.place_forget()
home_frames = []
home_frame_index = 0
home_anim_id = None


# image loading and background setting functions
def load_static(path):
    img = Image.open(path)
    img = img.resize((1280, 720))
    return ImageTk.PhotoImage(img)

# set background image on canvas
def set_background(image_path):
    clear_hotspots()
    canvas.delete("all")
    canvas.bg = load_static(image_path)
    canvas.create_image(0, 0, anchor="nw", image=canvas.bg)

# load and prepare frames for home GIF animation
# since i want the home screen to be animated
def load_home_gif(path=home_gif):
    global home_frames, home_frame_index
    im = Image.open(path)
    frames = []
    for frame in ImageSequence.Iterator(im):
        frame = frame.resize((1280, 720))
        frames.append(ImageTk.PhotoImage(frame))
    home_frames = frames
    home_frame_index = 0

# animate home screen GIF
def animate_home():
    global home_frame_index, home_anim_id, home_frames
    if not home_frames:
        return
    frame = home_frames[home_frame_index]
    home_label.config(image=frame)
    home_frame_index = (home_frame_index + 1) % len(home_frames)
    home_anim_id = root.after(80, animate_home)

# this function stops home screen animation
def stop_home_animation():
    global home_anim_id
    if home_anim_id is not None:
        root.after_cancel(home_anim_id)
        home_anim_id = None
    home_label.config(image="")

# hotspot management functions 
# to create and clear clickable areas on the canvas
def clear_hotspots():
    global current_hotspots
    for item in current_hotspots:
        canvas.delete(item)
    current_hotspots = []

def create_hotspot(rect, command):
    x1, y1, x2, y2 = rect
    r = canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="", width=0)
    canvas.tag_bind(r, "<Button-1>", lambda e: command())
    current_hotspots.append(r)

# page display functions
# to switch between different screens of the app
def show_home():
    canvas.place_forget()
    stop_home_animation()
    home_label.place(x=0, y=0, width=1280, height=720)
    load_home_gif(home_gif)
    animate_home()
    home_label.bind("<Button-1>", home_click)

def show_canvas_background(path):
    stop_home_animation()
    home_label.place_forget()
    canvas.place(x=0, y=0)
    set_background(path)

# navigation functions for each screen
def go_home():
    global scoreboard_widgets
    # destroy scoreboard widgets (if present)
    for widget in scoreboard_widgets:
        widget.destroy()
    scoreboard_widgets = []
    show_home()

# instructions screen
def go_instructions():
    show_canvas_background(instructions_img)
    clear_hotspots()
    canvas.bind("<Button-1>", instructions_click)

# difficulty selection screen
def go_difficulty():
    show_canvas_background(difficulty_img)
    clear_hotspots()
    canvas.bind("<Button-1>", difficulty_click)

# quiz screen
def go_quiz():
    global score, question_num
    show_canvas_background(quiz_bg_img)
    score = 0
    question_num = 0
    new_question()


# scoreboard screen
def go_scoreboard():
    global scoreboard_widgets
    show_canvas_background(scoreboard_img)
    clear_hotspots()
    
# cleanup quiz widgets  
    for widget in root.winfo_children():
        if isinstance(widget, (tk.Entry, tk.Label, tk.Button)) and widget not in [canvas, home_label]:
            widget.destroy()
    scoreboard_widgets = []  # clear previous widgets

    # display final score and grade
    score_label = canvas.create_text(640, 280, text=f"Final Score: {score} / 100",
                                     font=("Typewriter", 32, "bold"), fill="black")
    grade_label = canvas.create_text(640, 360, text=f"Grade: {rank_user(score)}",
                                     font=("Typewriter", 26), fill="black")

    # hotspot coordinates for your designed buttons
    play_coords = (550, 521, 734, 561)
    quit_coords = (540, 597, 730, 633)

    # create clickable hotspots
    create_hotspot(play_coords, go_home)
    create_hotspot(quit_coords, root.quit)


# click handling functions for each screen
def inside(x, y, rect):
    x1, y1, x2, y2 = rect
    return x1 <= x <= x2 and y1 <= y <= y2

def home_click(event):
    x, y = event.x, event.y
    if inside(x, y, home_rects["play"]): go_difficulty()
    elif inside(x, y, home_rects["instr"]): go_instructions()
    elif inside(x, y, home_rects["quit"]): root.quit()

def instructions_click(event):
    x, y = event.x, event.y
    if inside(x, y, instructions_rects["back"]): go_home()

def difficulty_click(event):
    global level
    x, y = event.x, event.y
    if inside(x, y, difficulty_rects["easy"]): level = "easy"; go_quiz()
    elif inside(x, y, difficulty_rects["moderate"]): level = "moderate"; go_quiz()
    elif inside(x, y, difficulty_rects["advanced"]): level = "advanced"; go_quiz()
    elif inside(x, y, difficulty_rects["back"]): go_home()

def scoreboard_click(event):
    go_home()

# quiz question generation and answer checking functions
def random_int():
    if level == "easy": return random.randint(1, 9)
    if level == "moderate": return random.randint(10, 99)
    return random.randint(100, 999)

# generate a new math question 
# addition or subtraction based on selected difficulty

def generate():
    global num1, num2, answer, operation
    num1 = random_int()
    num2 = random_int()

    # randomly choose addition or subtraction
    operation = random.choice(["+", "-"])

    if operation == "+":
        answer = num1 + num2
    else:
        # prevent negative results
        if num2 > num1:
            num1, num2 = num2, num1
        answer = num1 - num2

# display new question
def new_question():
    global question_num, attempt, entry, feedback_text
    question_num += 1
    attempt = 1

    if question_num == 11:  # end of quiz
        go_scoreboard()
        return

    clear_hotspots()
    canvas.delete("all")
    canvas.bg = load_static(quiz_bg_img)
    canvas.create_image(0, 0, anchor="nw", image=canvas.bg)


    generate() # create new question

    canvas.create_text(640, 220, text=f"QUESTION {question_num} / 10",
                       font=("Typewriter", 32), fill="black")
    canvas.create_text(640, 300, text=f"{num1} {operation} {num2}",
                       font=("Typewriter", 60), fill="black")

    entry = tk.Entry(root, font=("Typewriter", 32), justify="center", width=6, fg="black")
    canvas.create_window(640, 380, window=entry)

    submit_btn = tk.Button(root, text="SUBMIT", font=("Typewriter", 22),
                           command=check_answer,
                           bg="white", fg="black",
                           bd=1, relief="groove", cursor="hand2")
    canvas.create_window(640, 440, window=submit_btn)

    # create a canvas text object for feedback (initially empty)
    feedback_text = canvas.create_text(640, 500, text="", font=("Typewriter", 24), fill="black")

# check user's answer
def check_answer():
    global score, attempt
    try:
        user = int(entry.get())
    except Exception:
        canvas.itemconfig(feedback_text, text="ENTER A NUMBER", fill="red")
        return
# compare answer
    if user == answer:
        points = 10 if attempt == 1 else 5
        score += points
        msg = "PERFECT!" if attempt == 1 else "CORRECT (2nd TRY)"
        canvas.itemconfig(feedback_text, text=msg, fill="#11B63A")
        root.after(1200, new_question)
    else:
        if attempt == 1:
            attempt += 1
            canvas.itemconfig(feedback_text, text="TRY AGAIN", fill="#FFC300")
        else:
            canvas.itemconfig(feedback_text, text=f"ANSWER = {answer}", fill="#FF3333")
            root.after(1500, new_question)

# rank user based on final score
def rank_user(sc):
    if sc >= 90:
        return "A+"
    elif sc >= 80:
        return "A"
    elif sc >= 70:
        return "B"
    elif sc >= 60:
        return "C"
    elif sc >= 50:
        return "D"
    else:
        return "F"

# main program execution
go_home()
root.mainloop()
