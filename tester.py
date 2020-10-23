from monopoly import MonopolyEnv
import numpy as np
from time import sleep
import tkinter as tk


def decrease():
    value = int(lbl_value["text"])
    lbl_value["text"] = f"{value - 1}"


def increase():
    value = int(lbl_value["text"])
    lbl_value["text"] = f"{value + 1}"


myBoard = MonopolyEnv.MonopolyEnv(5)

window = tk.Tk()

frm_entry = tk.Frame(master=window)
ent_temperature = tk.Entry(master=frm_entry, width=10)
lbl_temp = tk.Label(master=frm_entry, text="\N{DEGREE FAHRENHEIT}")

btn_decrease = tk.Button(master=window, text="-", command=decrease)

lbl_value = tk.Label(master=window, text="0")

btn_increase = tk.Button(master=window, text="+", command=increase)


ent_temperature.grid(row=0, column=0, sticky="w")
lbl_temp.grid(row=0, column=1, sticky="w")
frm_entry.grid(row=0, column=0, padx=10)
btn_decrease.grid(row=1, column=0, sticky="nsew")
lbl_value.grid(row=1, column=1)
btn_increase.grid(row=1, column=2, sticky="nsew")

# Create an event handler
def handle_keypress(event):
    """Print the character associated to the key pressed"""
    print(event.char)

window.bind("<Key>", handle_keypress)


window.mainloop()


