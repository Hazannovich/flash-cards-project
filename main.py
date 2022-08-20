import pandas
import random
import time
from tkinter import *

BACKGROUND_COLOR = "#B1DDC6"

# ---------------------------------------Data Reading-----------------------------------d #
current_card = {}
to_learn = {}

try:
    words_data = pandas.read_csv(filepath_or_buffer="data/to_learn.csv")
except FileNotFoundError:
    original_words_data = pandas.read_csv(filepath_or_buffer="data/french_words.csv")
    to_learn = original_words_data.to_dict(orient="records")
else:
    to_learn = words_data.to_dict(orient="records")
    current_card = {}


# ---------------------------------------Generate New Word------------------------------ #
def next_card():
    global current_card, flip_timer
    win.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    fr_word = current_card["French"]
    canvas.itemconfig(card, image=front_img)
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word, text=fr_word, fill="black")
    flip_timer = win.after(3000, func=flip_card)


# ---------------------------------------Flip Card-------------------------------------- #
def flip_card():
    global current_card
    en_word = current_card["English"]
    canvas.itemconfig(card, image=back_img)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=en_word, fill="white")


def remove_word():
    global current_card
    to_learn.remove(current_card)
    df = pandas.DataFrame(to_learn)
    df.to_csv("data/to_learn.csv", index=False)
    next_card()


# ---------------------------------------UI SETUP---------------------------------------- #

# Canvas
win = Tk()
win.title("Memory Cards")
win.config(bg=BACKGROUND_COLOR, highlightthickness=0, padx=50, pady=50)
flip_timer = win.after(3000, func=flip_card)
front_img = PhotoImage(file="./images/card_front.png")
back_img = PhotoImage(file="./images/card_back.png")
canvas = Canvas(win, width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card = canvas.create_image(400, 263, image=front_img)
title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"), )
canvas.grid(column=0, row=0, columnspan=2)

# Buttons
right_btn_img = PhotoImage(file="./images/right.png")
right_btn = Button(image=right_btn_img, highlightthickness=0, command=remove_word)
right_btn.grid(column=1, row=1)
wrong_btn_img = PhotoImage(file="./images/wrong.png")
wrong_btn = Button(image=wrong_btn_img, highlightthickness=0, command=next_card)
wrong_btn.grid(column=0, row=1)

next_card()
win.mainloop()
