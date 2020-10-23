from monopoly.Board import Board
from monopoly.Player import Player
import numpy as np
import cv2
from PIL import Image, ImageDraw
from time import sleep

class MonopolyEnv:

    def __init__(self, player_num):
        self.board = Board(player_num)
        self.curr_player = 0
        self.player_num = player_num
        self.players = []
        self.moved = False
        for i in range(player_num):
            self.players.append(Player(i))

    def move(self, position):
        if not self.moved:
            self.players[self.curr_player].move(position)
            self.board.set_pos(self.curr_player, self.players[self.curr_player].get_pos())
            self.moved = True

    def end_turn(self):
        if self.moved:
            if self.player_num-1 > self.curr_player:
                self.curr_player += 1
            else:
                self.curr_player = 0
            self.moved = False

    def run(self):
        for j in range(10):
            for i in range(self.player_num):
                rnd = np.random.randint(1, 7)
                rnd1 = np.random.randint(1, 7)
                self.move(i, rnd + rnd1)
                self.render()

    def render(self, delay=1000):
        return self.board.get_image().resize((900,900))
        #self.root.after(delay, self.render)

    def get_current_ply(self):
        return self.curr_player

    def get_money(self):
        return self.players[self.curr_player].get_money()

    def get_pos(self):
        return self.players[self.curr_player].get_pos()

    def buy(self, price = -1):
        field = self.board.get_field_ptr(self.get_pos())
        self.players[self.curr_player].buy(field, price)


    def possible_actions(self):
        actions = []
        pos = self.get_pos()
        field_type = self.board.get_field_type(pos)
        if field_type == "Property" or field_type == "Transport" or field_type == "Service":
            if not self.board.has_owner(pos) and self.get_money() > self.board.get_price(pos):
                actions.append(["buy", self.board.get_price(pos)])
            elif self.board.get_owner(pos) != self.curr_player:
                actions.append(["pay rent ", self.board.get_rent(pos)])
        elif field_type == "Luxury_tax" :
                actions.append(["pay tax", 100])
        elif field_type == "Income_tax":
            actions.append(["pay tax", 200])
        build_colors = self.players[self.curr_player].get_buildable_colors()
        for bc in build_colors:
            actions.append(["build house ", bc])

        return actions
