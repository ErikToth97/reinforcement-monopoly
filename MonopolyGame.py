from monopoly.MonopolyEnv import MonopolyEnv
import numpy as np
from time import sleep
from PIL import ImageTk, Image
import tkinter as tk
from functools import partial
import cv2


class MonopolyGame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=False)
        self.monopolyEnv = MonopolyEnv(5)
        self.dice_val = 0
        self.label_texts = []
        self.action_buttons = []
        for i in range(5):
            self.label_texts.append(tk.StringVar())
        self.create_widgets()



    def create_widgets(self):
        self.upper_info_frame = tk.Frame(self)
        self.upper_info_frame.pack(side="top", fill=tk.X, padx=5, pady=5)

        self.label_texts[0].set("Player: "+str(self.monopolyEnv.get_current_ply()))
        self.ply_num = tk.Label(self.upper_info_frame, textvariable=self.label_texts[0])
        self.ply_num.pack(side="left")

        self.label_texts[1].set("Money: " + str(self.monopolyEnv.get_money()))
        self.ply_money = tk.Label(self.upper_info_frame, textvariable=self.label_texts[1])
        self.ply_money.pack(side="left")

        self.label_texts[2].set("Dice: " + str(self.dice_val))
        self.ply_dice = tk.Label(self.upper_info_frame, textvariable=self.label_texts[2])
        self.ply_dice.pack(side="left")


        self.upper_button_frame = tk.Frame(self)
        self.upper_button_frame.pack(side="top", fill=tk.X, padx=5, pady=5)

        self.move_bt = tk.Button(self.upper_button_frame)
        self.move_bt["text"] = "Throw dice"
        self.move_bt["command"] = self.dice
        self.move_bt.pack(side="left")

        self.quit = tk.Button(self.upper_button_frame, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="right", padx=5, pady=5)

        self.move_bt = tk.Button(self.upper_button_frame)
        self.move_bt["text"] = "End turn"
        self.move_bt["command"] = self.monopolyEnv.end_turn
        self.move_bt.pack(side="right")

        #cv2.imshow("img", np.array(self.monopolyEnv.render()))
        self.img = ImageTk.PhotoImage(self.monopolyEnv.render())
        self.panel = tk.Label(root, image=self.img)
        self.panel.pack(side="bottom", fill="both")

    def update_table(self):
        self.make_action_buttons()
        self.draw_img()
        self.label_texts[0].set("Player: "+str(self.monopolyEnv.get_current_ply()))
        self.label_texts[1].set("Money: " + str(self.monopolyEnv.get_money()))
        self.label_texts[2].set("Dice: " + str(self.dice_val))

    def make_action_buttons(self):

        for button in self.action_buttons:
            button.pack_forget()

        pos_actions = self.monopolyEnv.possible_actions()
        for pos_action in pos_actions:
            if pos_action[0] == "buy":
                self.action_buttons.append(tk.Button(self.upper_button_frame))
                self.action_buttons[-1]["text"] = "Buy for "+str(pos_action[1])
                self.action_buttons[-1]["command"] =lambda price= pos_action[1]: self.buy_prop(price)
                self.action_buttons[-1].pack(side="left")

    def buy_prop(self, price):
        self.monopolyEnv.buy(price)
        self.update_table()

    def draw_img(self):
        self.img = ImageTk.PhotoImage(self.monopolyEnv.render())
        self.panel.config(image=self.img)

    def dice(self):
        rnd1 = np.random.randint(1,6)
        rnd2 = np.random.randint(1,6)
        self.dice_val = rnd1+rnd2
        self.monopolyEnv.move(self.dice_val)
        self.update_table()


root = tk.Tk()
app = MonopolyGame(master=root)
app.mainloop()
