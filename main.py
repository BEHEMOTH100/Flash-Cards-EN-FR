#------------------------ IMPORTS ------------------------#
from tkinter import *
import pandas
from random import choice
BACKGROUND_COLOR = "#697565"
original_lang = "French"
translated_lang = "English"
curr_card = {}
to_learn = {}
#------------------------ DATAFRAME ------------------------#
try:
    data = pandas.read_csv("./words-data/not-yet-known-words.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("words-data/original-words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")
#------------------------ SAVE PROGRESS ------------------------#
def is_known():
    to_learn.remove(curr_card)
    df = pandas.DataFrame(to_learn)
    df.to_csv("./words-data/not-yet-known-words.csv", index=False)

    next_card()
# ------------------------ RESET PROGRESS ------------------------#
def reset_progress():
    try:
        with open(file="./words-data/original-words.csv", mode="r") as origin_file:
            origin_data = origin_file.read()
    except FileNotFoundError:
        print("File not found")
    else:
        with open(file="./words-data/not-yet-known-words.csv", mode="w") as f:
            f.write(origin_data)
        quit()
#------------------------ NEXT CARD ------------------------#
def next_card():
    global curr_card, flip_timer
    reset_button.config(text=f"RESET {len(to_learn)} words left")
    window.after_cancel(flip_timer)
    flip_timer = window.after(3500, flipping_card)

    curr_card = choice(to_learn)
    canvas.itemconfig(language_text,fill="black", text=f"{translated_lang}")
    canvas.itemconfig(word_text,fill="black", text=curr_card[f"{translated_lang}"])
    canvas.itemconfig(card_canvas, image=card_front_img)
#------------------------ FLIPPING CARDS ------------------------#
def flipping_card():
    global curr_card
    canvas.itemconfig(card_canvas, image=card_back_img)
    canvas.itemconfig(language_text, fill="white", text=f"{original_lang}")
    canvas.itemconfig(word_text, fill="white", text=curr_card[f"{original_lang}"])
#------------------------ SEE CARD AGAIN ------------------------#
def see_card_again():
    global curr_card, flip_timer
    window.after_cancel(flip_timer)
    flip_timer = window.after(3500, flipping_card)
    #english side of card
    canvas.itemconfig(language_text, fill="black", text=f"{translated_lang}")
    canvas.itemconfig(word_text, fill="black", text=curr_card[f"{translated_lang}"])
    canvas.itemconfig(card_canvas, image=card_front_img)
    #flips after a while to french side
# ------------------------ Flip languages ------------------------#
def flip_language():
    global original_lang
    global translated_lang
    if original_lang == "French":
        original_lang = "English"
        translated_lang = "French"
        right_button_label.config(text="Je comprend ce mot")
        see_again_button.config(text="Voir encore")
    elif original_lang == "English":
        right_button_label.config(text="I understand this word")
        see_again_button.config(text="See again")
    else:
        original_lang = "French"
        translated_lang = "English"
    see_card_again()
#------------------------ UI DESIGN ------------------------#
window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)


# creating images
right_button_img = PhotoImage(file="images/check.png")
x_button_img = PhotoImage(file="images/cross.png")
card_front_img = PhotoImage(file="images/card-front.png")
card_back_img = PhotoImage(file="images/card-back.png")
reset_img = PhotoImage(file="images/reset.png")
#----------------- UI FLASH CARDS -----------------#
#card
canvas = Canvas(width=800, height=526)
card_canvas = canvas.create_image(400, 263, image=card_front_img)
canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
language_text = canvas.create_text(400, 150, text="", font=("Ariel", 30, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Ariel", 40, "bold"))
canvas.grid(row=1, column=0, columnspan=5)

#buttons
right_button = Button(image=right_button_img, highlightthickness=0, command=is_known, background=BACKGROUND_COLOR)
right_button.grid(row=2, column=3)

x_button = Button(image=x_button_img, highlightthickness=0, command=next_card, background=BACKGROUND_COLOR)
x_button.grid(row=2, column=2)

reset_button = Button( text=f"RESET", foreground="black", highlightthickness=0, command=reset_progress)
reset_button.grid(row=0, column=2)

see_again_button = Button(text="See again", foreground="black", highlightthickness=0, command=see_card_again)
see_again_button.grid(row=1, column=6)

flip_lang_button = Button(text="Flip", foreground="black", highlightthickness=0, command=flip_language)
flip_lang_button.grid(row=0, column=3)

#labels
right_button_label = Label(text="I understand this one", font=("courier", 15, "normal"), background=BACKGROUND_COLOR, foreground="black")
right_button_label.grid(row=3, column=3)



flip_timer = window.after(3500, flipping_card)
next_card()


window.mainloop()