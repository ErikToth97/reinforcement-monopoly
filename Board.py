import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageTk
from monopoly.Property import Property
from monopoly.Service import Service
from monopoly.Transport import Transport
from monopoly.Player import Player
import tkinter


class Board:
    def __init__(self, player_num):
        self.table = [0] * 40
        self.color_table = [0]*40
        self.colors = {
            "brown": (52,79,126),
            "light_blue": (247,210,136),
            "pink": (255,0,255),
            "orange": (0, 128,255),
            "red": (0,0,200),
            "yellow": (0,255,255),
            "green": (0,200,0),
            "dark_blue": (128,0,0),
            "Start": (0,0,0),
            "Income_tax": (0,128,128),
            "Luxury_tax": (0,128,128),
            "Visit": (255,255,255),
            "Jail": (255,0,128),
            "Parking": (192, 192, 192),
            "service": (192,128,255),
            "transport": (128,128,64),
            "Chest": (7,211,248),
            "Chance": (255,128,255)
        }
        self.player_num = player_num
        self.players = [0]*player_num
        self.properties = {
            "brown": {"tile": [1, 3], "price": [60, 60],
                      "rents": [[2, 10, 30, 90, 160, 250],
                                [4, 20, 60, 180, 320, 450]],
                      "house_price": 50,},
            "light_blue": {"tile": [6, 8, 9], "price": [100, 100, 120],
                           "rents": [[6, 30, 90, 270, 400, 550],
                                     [6, 30, 90, 270, 400, 550],
                                     [8, 40, 100, 300, 450, 600]],
                           "house_price": 50},
            "pink": {"tile": [11, 13, 14], "price": [140, 140, 160],
                     "rents": [[10, 50, 150, 450, 625, 750],
                               [10, 50, 150, 450, 625, 750],
                               [12, 60, 180, 500, 700, 900]],
                     "house_price": 100},
            "orange": {"tile": [16, 18, 19], "price": [180, 180, 200],
                       "rents": [[14, 70, 200, 550, 750, 950],
                                 [14, 70, 200, 550, 750, 950],
                                 [16, 80, 220, 600, 800, 1000]],
                       "house_price": 100},
            "red": {"tile": [21, 23, 24], "price": [220, 220, 240],
                    "rents": [[18, 90, 250, 700, 875, 1050],
                              [18, 90, 250, 700, 875, 1050],
                              [20, 100, 300, 750, 925, 1100]],
                    "house_price": 150},
            "yellow": {"tile": [26, 27, 29], "price": [260, 260, 280],
                       "rents": [[22, 110, 330, 800, 975, 1150],
                                 [22, 110, 330, 800, 975, 1150],
                                 [24, 110, 330, 800, 975, 1150]],
                       "house_price": 150},
            "green": {"tile": [31, 32, 34], "price": [300, 300, 320],
                      "rents": [[26, 130, 390, 900, 1100, 1275],
                                [26, 130, 390, 900, 1100, 1275],
                                [28, 150, 450, 100, 1200, 1400]],
                      "house_price": 200},
            "dark_blue": {"tile": [37, 39], "price": [350, 400],
                          "rents": [[35, 175, 500, 1100, 1300, 1500],
                                    [50, 200, 600, 1400, 1700, 2000]],
                          "house_price": 200},
        }
        self.services = [12, 28]
        self.transports = [5, 15, 25, 35]
        self.cards = {
            "Chest": [2, 17, 33],
            "Chance": [7, 22, 36]
        }
        self.player_colors = ['blue', 'yellow', 'brown', 'red', 'orange', 'white']


        for key, prop in self.properties.items():
            ct = 0

            for ti in prop["tile"]:
                print(key)
                self.table[ti] = Property(prop["price"][ct], prop["rents"][ct], len(prop["tile"]), prop["house_price"], key)
                self.color_table[ti] = self.colors[key]
                ct += 1

        sv = 0
        for service in self.services:
            self.table[service] = Service(sv)
            self.color_table[service] = self.colors["service"]
            sv += 1

        sv = 0
        for transport in self.transports:
            self.table[transport] = Transport(sv)
            self.color_table[transport] = self.colors["transport"]
            sv += 1
        for key, card in self.cards.items():
            for num in card:
                self.table[num] = key
                self.color_table[num] = self.colors[key]

        self.table[0] = "Start"
        self.color_table[0] = self.colors["Start"]
        self.table[4] = "Income_tax"
        self.color_table[4] = self.colors["Income_tax"]
        self.table[10] = "Visit"
        self.color_table[10] = self.colors["Visit"]
        self.table[20] = "Parking"
        self.color_table[20] = self.colors["Parking"]
        self.table[30] = "Jail"
        self.color_table[30] = self.colors["Jail"]
        self.table[38] = "Luxury_tax"
        self.color_table[38] = self.colors["Luxury_tax"]



    def set_pos(self, player_num, pos):
        self.players[player_num] = pos

    def get_field_type(self, pos):
            if isinstance(self.table[pos], str):
                return self.table[pos]
            else:
                return self.table[pos].get_type()

    def has_owner(self, pos):
        return self.table[pos].is_owned()

    def get_owner(self, pos):
        return self.table[pos].get_owner()

    def get_rent(self, pos):
        return self.table[pos].get_rent()

    def get_price(self, pos):
        return self.table[pos].get_price()

    def get_field_ptr(self, pos):
        return self.table[pos]

    # FOR CNN #
    def get_image(self):
        env = np.zeros((11, 11, 3), dtype=np.uint8)
        for i in range(11):
            for j in range(11):
                if i == 0:
                    env[10-i, 10-j] = self.color_table[j]
                elif i == 10:
                    env[10 - i, 10 - j] = self.color_table[30-j]
                elif j == 0:
                    env[10 - i, 10 - j] = self.color_table[40 - i]
                elif j == 10:
                    env[10 - i, 10 - j] = self.color_table[10+i]
                else:
                    env[10-i, 10-j] = (255,255,255)

        img = Image.fromarray(env, 'RGB')

        width = 968
        height = 968
        img = img.resize((width, height), resample=0)
        img = img.rotate(180)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        draw = ImageDraw.Draw(img)
        vert_lines = 11
        hor_lines = 11

        for i in range(1, vert_lines):
            draw.line((width // vert_lines * i, 0, width // vert_lines * i, img.size[1]), fill=0)
        for i in range(1, hor_lines):
            draw.line((0, height // hor_lines * i, img.size[0], height // hor_lines * i), fill=0)
        ct = 0


        for ply in range(self.player_num):
            position = self.players[ply]
            if position < 11:
                if ct < 3:
                    posX = 10 + ct * 29 + position * 88
                    posY = 20
                    ct += 1
                elif ct < 6:
                    posX = 10 + (ct - 3) * 29 + position * 88
                    posY = 50
                    ct += 1
            elif position < 21:
                if ct < 3:
                    posX = 10 + ct * 29 + 10 * 88
                    posY = 20 + (position - 10) * 88
                    ct += 1
                elif ct < 6:
                    posX = 10 + (ct - 3) * 29 + 10 * 88
                    posY = 50 + (position - 10) * 88
                    ct += 1
            elif position < 31:
                if ct < 3:
                    posX = 10 + ct * 29 + (30 - position) * 88
                    posY = 20 + 10 * 88
                    ct += 1
                elif ct < 6:
                    posX = 10 + (ct - 3) * 29 + (30 - position) * 88
                    posY = 50 + 10 * 88
                    ct += 1
            else:
                if ct < 3:
                    posX = 10 + ct * 29
                    posY = 20 + (40 - position) * 88
                    ct += 1
                elif ct < 6:
                    posX = 10 + (ct - 3) * 29
                    posY = 50 + (40 - position) * 88
                    ct += 1
            draw.ellipse((posX, posY, posX + 13, posY + 13), fill=self.player_colors[ct - 1], outline='red')
        return img #cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
