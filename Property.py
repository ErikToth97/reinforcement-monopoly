from monopoly.BuyableLand import BuyableLand


class Property(BuyableLand):
    def __init__(self, price, rents, num_of_color, price_of_house, color):
        super().__init__(price, rents, num_of_color, "Property")
        self.price_of_house = price_of_house
        self.houses = 0
        self.hotel = False
        self.color = color

    def get_rent(self):
        multiplier = 1
        if self.houses == 0:
            multiplier = 2
        if not self.hotel:
            if self.owned_num == self.num_of_color:
                return self.rents[self.houses] * multiplier
            else:
                return self.rents[0]
        else:
            return self.rents[-1]

    def build(self, num_of_house):
        if self.houses < 4:
            self.houses += 1
        elif not self.hotel:
            self.hotel = True
            self.houses = 0
        else:
            return False
        return True

    def sell_house(self, amount):
        if not self.hotel:
            if self.houses >= amount:
                self.houses -= amount
                return True
            else:
                return False
        elif amount == 1:
            self.hotel = False
            return True
        else:
            return False

    def got_hotel(self):
        return self.hotel

    def get_color(self):
        return self.color

    def get_house_num(self):
        return self.houses+5*self.hotel

    def get_house_price(self):
        return self.price_of_house