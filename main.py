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
from paint_drying_sim import *
import tkinter as tk
from tkinter import messagebox
from os import path

root = tk.Tk()
root.title("Main")
root.config(bg="#232323")
root.geometry("800x600")

global_selected_difficulty = selected_difficulty
difficulty_var = tk.StringVar(root)
difficulty_var.set(global_selected_difficulty)

pds_button = None
placeholder_button = None

def difficulties():
    return difficulties_list

def clear_all_widgets():
    for tk_widget in root.winfo_children():
        tk_widget.destroy()

def load_main_menu():
    clear_all_widgets()
    root.title("Game Selector")
    global pds_button, placeholder_button
    pds_button = tk.Button(root, 
                   text="Paint Drying Sim", 
                   command = options_screen,
                   activebackground="#669361", 
                   activeforeground="white",
                   anchor="center",
                   bd=3,
                   bg="#3b6e36",
                   cursor="gobbler",
                   disabledforeground="gray",
                   fg="black",
                   font=("Arial", 12),
                   height=2,
                   highlightbackground="black",
                   highlightcolor="green",
                   highlightthickness=2,
                   justify="center",
                   overrelief="raised",
                   width=15,
                   wraplength=100)

    pds_button.pack(padx = 10, pady = 10)

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
    root.withdraw()
    try:
        g = Game(global_selected_difficulty)
        g.new()
        g.run()
    except:
        messagebox.showerror("Error", "Whoops. This didn't work.")
    root.deiconify()
    load_main_menu()

def launch_game():
    get_selected_difficulty()
    run_game()

def options_screen():
    clear_all_widgets()

    root.title("Difficulty Selector")

    opts_label = tk.Label(root, text = "Select Difficulty", font = ("Arial", 16), fg = "#000000", bg = "#E5C837", width = 20, height = 4, cursor = "pirate")
    opts_label.pack(padx = 20)

    difficulty_selection_radiobuttons_frame = tk.Frame(root, bg = "#2A2885", width = 1000)
    difficulty_selection_radiobuttons_frame.pack(fill = "x", padx = 25)

    for difficulty in difficulties():
        tk.Radiobutton(difficulty_selection_radiobuttons_frame, text = difficulty, variable = difficulty_var, value = difficulty, font = ("Arial", 14), cursor = "hand2", fg = "#000000", bg = "#2A2885", activebackground = "#4A4880").pack(anchor = "w", padx = 50, pady = 10)
    
    button_frame = tk.Frame(root, bg = "#1C1B52")
    button_frame.pack()

    continue_button = tk.Button(button_frame, text = "Continue", command = launch_game, font = ("Arial", 12), width = 20, cursor = "sb_right_arrow", bg = "#2E863A", fg = "#FFFFFF", activebackground = "#4F9758")
    continue_button.pack(side = "right", padx = 20, pady = 20)

    back_button = tk.Button(button_frame, text = "Back", command = load_main_menu, font = ("Arial", 12), width = 20, cursor = "sb_left_arrow", bg = "#DC5151", fg = "#FFFFFF", activebackground = "#E27E7E")
    back_button.pack(side = "left", padx = 20, pady = 20)

def placeholder_cmd():
    print('click \nThis doesn\'t seem to do anything...')

load_main_menu()

root.mainloop()