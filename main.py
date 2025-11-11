# Created by Emmanuel Swenson

# yay I can use github from VS CODE!

# Scources
'''
https://www.geeksforgeeks.org/python/python-gui-tkinter/#
https://www.geeksforgeeks.org/python/python-creating-a-button-in-tkinter/
https://www.geeksforgeeks.org/python/python-tkinter-messagebox-widget/
'''

# import necessary modules
import math
import random
import sys
import pygame as pg
from settings import *  # the starting values of variables and constants
from sprites import *  # defining the characters / objects (player, mob, etc.)
from utils import *  # defining the characteristics of the maps
from paint_drying_clicker import *
from paint_drying_sim import *
import tkinter as tk
from tkinter import messagebox
from os import path

# making the main window
root = tk.Tk()
root.title("Main")
root.config(bg="#232323")
root.geometry("800x600")

# difficulty for paint drying sim
global_selected_difficulty = selected_difficulty
difficulty_var = tk.StringVar(root)
difficulty_var.set(global_selected_difficulty)

pds_button = None
placeholder_button = None

global clicks, countdown
clicks = 0
countdown = 100

def difficulties():
    return difficulties_list

def clear_all_widgets(): # clears the window
    for tk_widget in root.winfo_children():
        tk_widget.destroy()

def load_main_menu(): # loads the games menu
    clear_all_widgets()
    root.title("Game Selector")
    global pds_button, placeholder_button
    pds_button = tk.Button(root, # where it is placed
                   text="Paint Drying Sim", # what the button says
                   command = options_screen, # what it does when clicked
                   activebackground="#669361", # when clicked bg
                   activeforeground="white", # when clicked text color
                   anchor="center", # positioning in the window
                   bd=3, # border amount
                   bg="#3b6e36", # bg when not active
                   cursor="gobbler", # mouse sprite when hovering over the button
                   disabledforeground="gray", # text color when button is disabled
                   fg="black", # text color when not active
                   font=("Arial", 12), # font and font size of text
                   height=2, # heignt of the button
                   highlightbackground="black", # color of border around the widget
                   highlightcolor="green", # border color when actively selected
                   highlightthickness=2, # width/height of the border
                   justify="center", # text positioning in the button
                   overrelief="raised", # relief style (goes in/out; only for button widget)
                   width=15, # width of the button
                   wraplength=100) # max length of text (in pixels) befor it is wrapped to the next line

    pds_button.pack(padx = 10, pady = 10) # .pack makes the button appear on the window (.grid can also be used)

    placeholder_button = tk.Button(root,
                                text = "Placeholder",
                                command = placeholder_cmd,
                                bd = 3,
                                cursor = "question_arrow",
                                font = ("Arial", 12),
                                height = 2,
                                justify = "center",
                                width = 15,
                                wraplength = 100)

    paint_clicker_button = tk.Button(root,
                                     text = "Paint Drying Clicker",
                                     command = run_game,
                                     bd = 3,
                                     cursor = "spraycan",
                                     font = ("Arial", 12),
                                     height = 2,
                                     justify = "center",
                                     width = 15,
                                     wraplength = 100,
                                     bg = "#80633A",
                                     fg = "#FFFFFF",
                                     activebackground = "#9D8665")

    paint_clicker_button.pack(padx = 10, pady = 10) # padx and pady are the padding horizontally and vertcally around a widget

    placeholder_button.pack(padx = 10, pady = 10)

    quit_button = tk.Button(root,
                            text = "Quit",
                            command = root.destroy,
                            bg="#b43c3c",
                            fg = "#FFFFFF",
                            activebackground = "#c37272",
                            bd = 3,
                            cursor = "X_cursor",
                            font = ("Arial", 12),
                            height = 2,
                            justify = "center",
                            width = 15,
                            wraplength = 100)
    
    quit_button.pack(padx = 10, pady = 10)

def get_selected_difficulty():
    global global_selected_difficulty
    global_selected_difficulty = difficulty_var.get()

def run_game():
    root.withdraw() # hides root window
    try: # tries to run the game
        g = Game(global_selected_difficulty)
        g.new()
        g.run()
    except: # if an error occurs, informs user instead of breaking
        messagebox.showerror("Error", "Whoops. This didn't work.")
    root.deiconify() # brings root window back into view
    load_main_menu()

def launch_game(): # runs game with the selected difficulty
    get_selected_difficulty()
    run_game()

def options_screen(): # creates the options screen for paint drying sim
    clear_all_widgets()

    root.title("Difficulty Selector")

    opts_label = tk.Label(root, text = "Select Difficulty", font = ("Arial", 16), fg = "#000000", bg = "#E5C837", width = 20, height = 4, cursor = "pirate")
    opts_label.pack(padx = 20)

    # frame adds an area around a widget
    difficulty_selection_radiobuttons_frame = tk.Frame(root, bg = "#2A2885", width = 1000)
    difficulty_selection_radiobuttons_frame.pack(fill = "x", padx = 25) # fill "x" makes the screen stretch from one side of the window to the ohter

    # creates a radiobutton for each difficulty option
    for difficulty in difficulties():
        tk.Radiobutton(difficulty_selection_radiobuttons_frame, text = difficulty, variable = difficulty_var, value = difficulty, font = ("Arial", 14), cursor = "hand2", fg = "#000000", bg = "#2A2885", activebackground = "#4A4880").pack(anchor = "w", padx = 50, pady = 10)
    
    button_frame = tk.Frame(root, bg = "#1C1B52")
    button_frame.pack()

    continue_button = tk.Button(button_frame, text = "Continue", command = launch_game, font = ("Arial", 12), width = 20, cursor = "sb_right_arrow", bg = "#2E863A", fg = "#FFFFFF", activebackground = "#4F9758")
    continue_button.pack(side = "right", padx = 20, pady = 20)

    back_button = tk.Button(button_frame, text = "Back", command = load_main_menu, font = ("Arial", 12), width = 20, cursor = "sb_left_arrow", bg = "#DC5151", fg = "#FFFFFF", activebackground = "#E27E7E")
    back_button.pack(side = "left", padx = 20, pady = 20)

def placeholder_cmd(): # secret dialog
    global clicks
    global countdown
    clicker_button_shown = (clicks == 200)
    if clicks == 0:
        messagebox.showinfo("???","This doesn't seem to do anything...")
    elif clicks == 1:
        messagebox.showinfo("???", "Nothing happens...")
    elif clicks == 2:
        messagebox.showinfo("???", "I told you this doesn't do anything.")
    elif clicks == 3:
        messagebox.showinfo("???","How many times do I have to tell you this doesn't do anything!?")
    elif clicks == 4:
        messagebox.showinfo("???","...")
    elif clicks == 5:
        messagebox.showwarning("???","Dont't click this button again!")
    elif clicks == 6:
        messagebox.showwarning("???","I'm gonna tell Microsoft to shut down your computer!")
    elif clicks == 7:
        messagebox.showwarning("???","OK! I'm gonna do it!")
    elif clicks == 8:
        messagebox.showwarning("???","Last chance!")
    elif clicks == 9:
        messagebox.showwarning("???","MICROSOFT!!!")
    elif clicks == 10 or clicks == 11 or clicks == 13 or clicks == 18 or clicks == 27 or clicks == 30 or clicks == 32 or clicks == 33 or clicks == 35 or clicks == 46 or clicks == 153 or clicks == 177:
        messagebox.showinfo("???","...")
    elif clicks == 12:
        messagebox.showinfo("???","I guess they might be busy right now...")
    elif clicks == 14:
        messagebox.showinfo("???","Can you please just stop clicking this button?")
    elif clicks == 15:
        messagebox.showinfo("???","Please???")
    elif clicks == 16:
        messagebox.showinfo("???","Seriously. STOP CLICKING.")
    elif clicks == 17:
        messagebox.showinfo("???","OMG. I've never seen someone so stubborn before.")
    elif clicks == 19:
        messagebox.askquestion("???","OK, how about this: I'll give you 10 coins if you stop right now.")
    elif clicks == 20:
        messagebox.askquestion("???","No? ok ok how about 100 coins.")
    elif clicks == 21:
        messagebox.showinfo("???","For heaven's sake please stop clicking this button.")
    elif clicks == 22:
        messagebox.askquestion("???","Alright, alright, how does 1,000 coins sound to you?")
    elif clicks == 23:
        messagebox.showinfo("???","I guess you just want to stay poor then.")
    elif clicks == 24:
        messagebox.askquestion("???","Are you sure you don't want the coins?")
    elif clicks == 25:
        messagebox.askquestion("???","Are you suuuure?")
    elif clicks == 26:
        messagebox.askquestion("???","Suuuuuuuuure???")
    elif clicks == 28:
        messagebox.showinfo("???","Welp, I was kidding about the coins anyway...")
    elif clicks == 29:
        messagebox.showinfo("???","Not like I would give you coins... they're waaaaay to precious.")
    elif clicks == 31:
        messagebox.askquestion("???","So... uh, how's life? Good?")
    elif clicks == 34:
        messagebox.askquestion("???","What even keeps you clicking this? You know this could go on forever, right?")
    elif clicks == 36:
        messagebox.askquestion("???","Do you want to hear a joke?")
    elif clicks == 37:
        messagebox.showinfo("???","Yes? Awesome! Get ready!")
    elif clicks == 38:
        messagebox.showinfo("???","What kind of music does a gold nugget listen to?")
    elif clicks == 39:
        messagebox.showinfo("???","Heavy Metal!!")
    elif clicks == 40:
        messagebox.showinfo("???","I know, very funny!")
    elif clicks == 41:
        messagebox.showinfo("???","Do you want to hear another one? I know you do!")
    elif clicks == 42:
        messagebox.showinfo("???","Why don't mining towns have hospitals?")
    elif clicks == 43:
        messagebox.showinfo("???","Because everyone there only suffers from MINER injuries!")
    elif clicks == 44:
        messagebox.showinfo("???","Enough jokes for now...")
    elif clicks == 45:
        messagebox.showinfo("???","I'm surprised you haven't left after those horrible jokes.")
    elif clicks == 47:
        messagebox.showinfo("???","OK then. I'm gonna count down from 100 and if you are still here when I'm done, I'm gonna be really angry.")
    elif clicks == 48:
        messagebox.showinfo("???","Here I go!")
    elif clicks == 49:
        messagebox.showinfo("???","I'm gonna start counting down now!")
    elif clicks >= 50 and clicks <= 150:
        messagebox.showinfo("???",f"{countdown}")
        countdown -= 1
    elif clicks == 151:
        messagebox.showinfo("???","Why are you still here? I've given you no reason to continue.")
    elif clicks == 152:
        messagebox.showinfo("???","I can't believe you were willing to click through 152 messageboxes already.")
    elif clicks == 154:
        messagebox.showinfo("???","Aren't you getting tired of this? 'Talking' to a nobody in a game?")
    elif clicks == 155:
        messagebox.showinfo("???","You don't even know my name.")
    elif clicks == 156:
        messagebox.showinfo("???","I guess I could tell you it.")
    elif clicks == 157:
        messagebox.showinfo("???","My name is No Name.")
    elif clicks == 158:
        messagebox.showinfo("???","Actually I don't have a name, hence 'No Name'.")
    elif clicks == 159:
        messagebox.showinfo("???","This is the best name - to not have a name.")
    elif clicks == 160:
        messagebox.showinfo("???","Think about it. It's impossible to make fun of my name because I don't have one!")
    elif clicks == 161:
        messagebox.showinfo("???","My mother was a genius for that! Just like me!")
    elif clicks == 162:
        messagebox.showinfo("???","I guess she got that from me.")
    elif clicks == 163:
        messagebox.showinfo("???","Actually, that doesn't make any sense...")
    elif clicks == 164:
        messagebox.showinfo("???","...I mean of course it does, because I'm a genius! Haha yeah...")
    elif clicks == 165:
        messagebox.askquestion("???","Anyways, I'm getting tired. Are you?")
    elif clicks == 166:
        messagebox.showinfo("???","I'm gonna go to sleep soon. You should too.")
    elif clicks == 167:
        messagebox.showinfo("???","Here take this cake.")
    elif clicks == 168:
        messagebox.askquestion("???","You say there's no cake?")
    elif clicks == 169:
        messagebox.showinfo("???","That's because the cake is a lie.")
    elif clicks == 170:
        messagebox.showinfo("???","I know. That was soooo funny.")
    elif clicks == 171:
        messagebox.showinfo("???","I hope that made you happy.")
    elif clicks == 172:
        messagebox.showinfo("???","Now, goodbye.")
    elif clicks == 173:
        messagebox.showinfo("???","This is the end.")
    elif clicks == 174:
        messagebox.showinfo("???","This is the end of our conversation.")
    elif clicks == 175:
        messagebox.showinfo("???","It's over!")
    elif clicks == 176:
        messagebox.showinfo("???","It is all over...")
    elif clicks == 178:
        messagebox.showinfo("???","You can stop talking to me now.")
    elif clicks == 179:
        messagebox.showinfo("???","You got exactly what you wanted from me, and it is now over.")
    elif clicks == 180:
        messagebox.showinfo("???","If you want to thank anyone, this is the time.")
    elif clicks == 181:
        messagebox.showinfo("???","Because it is done - it is over.")
    elif clicks == 182:
        messagebox.showinfo("???","Seriously, it's over.")
    elif clicks == 183:
        messagebox.showinfo("???","There is nothing else.")
    elif clicks >= 184 and clicks <= 193:
        messagebox.showinfo("???","...")
    elif clicks == 194:
        messagebox.showinfo("???","Hmm... you're still here.")
    elif clicks == 195:
        messagebox.showinfo("???","Man, you are very dedicated. This was a very long conversation.")
    elif clicks == 196:
        messagebox.showinfo("???","I don't know what to say.")
    elif clicks == 197:
        messagebox.showinfo("???","I'm sorry to say this, but there is nothing here.")
    elif clicks == 198:
        messagebox.showinfo("???","This is actually the end. I swear.")
    elif clicks == 199:
        messagebox.showinfo("???","This is my final goodbye!")
    elif clicks == 200:
        messagebox.showinfo("???","Goodbye!")
    else:
        messagebox.showinfo("???","No one responds... I guess the conversation really is over.")

    clicks += 1
    
    return clicks, countdown

load_main_menu()

root.mainloop() # required for window to appear; everything that appears in the window must be before 'root.mainloop()'