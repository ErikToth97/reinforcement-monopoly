from monopoly.Property import Property
from monopoly.Service import Service
from monopoly.Transport import Transport

class Player:
    def __init__(self, ply_num):
        self.position = 0
        self.money = 1500
        self.properties = set()
        self.services = set()
        self.transports = set()
        self.in_game = True
        self.ply_num = ply_num

    def buy(self, tile, price):
        if price == -1:
            price = tile.get_price()
        if self.money > price:
            self.money -= price
            if isinstance(tile, Property):
                self.properties.add(tile)
            elif isinstance(tile, Service):
                self.services.add(tile)
            else:
                self.transports.add(tile)
            tile.buy(self.ply_num)

    def sell(self, tile):
        if tile in self.properties:
            self.properties.remove(tile)
            self.money += tile.price
            tile.sell()

    def move(self, position):
        if self.position + position < 40:
            self.position += position
        else:
            self.position = self.position+position-40
        return self.position

    def pay(self, rent):
        if self.money > rent:
            self.money -= rent
            return rent
        else:
            self.in_game = False
            return self.money

    def get_rent(self, rent):
        self.money += rent

    def buy_house(self, tile, num_of_houses):
        if tile in self.properties:
            all_of_color = []
            for i in range(len(self.properties)):
                if tile != self.properties[i] and tile.get_color == self.properties[i].get_color:
                    all_of_color.append(self.properties[i].get_house_num())

            can_buy = True
            for i in range(len(all_of_color)):
                if tile.get_house_num + num_of_houses > all_of_color[i]+1:
                    can_buy = False
            if(can_buy):
                tile.build(num_of_houses)
                self.money -= tile.get_house_price()*num_of_houses

    def sell_house(self, tile, num_of_houses):
        if tile in self.properties:
            if not tile.got_hotel():
                tile.sell_house(num_of_houses)
                self.money += tile.price_of_house*num_of_houses//2
            else:
                tile.sell_house(1)
                self.money += tile.price_of_house//2

    def get_pos(self):
        return self.position

    def get_money(self):
        return self.money

    def get_buildable_colors(self):
        colors = ["brown", "light_blue", "pink", "orange", "red", "yellow", "green", "dark_blue"]
        ret = []
        for color in colors:
            counter = 0
            num_needed = -1
            for prop in self.properties:
                if color == prop.get_color():
                    counter += 1
                    num_needed = prop.get_num_of_color()

            if num_needed == counter:
                ret.append(color)

        return ret
