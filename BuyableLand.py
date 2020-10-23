class BuyableLand:
    def __init__(self, price, rents, num_of_color, tile_type):
        self.price = price
        self.rents = rents
        self.num_of_color = num_of_color
        self.owned_num = 0
        self.mortgage = False
        self.owned = False
        self.owner = None
        self.tile_type = tile_type

    def get_rent(self):
        pass

    def get_mortgage(self):
        if not self.mortgage:
            self.mortgage = True
            return True
        else:
            return False

    def pay_mortgage(self):
        if self.mortgage:
            self.mortgage = False
            return True
        else:
            return False

    def buy(self, owner):
        if not self.owned:
            self.owned = True
            self.owner = owner
            return True
        else:
            return False

    def sell(self):
        if self.owned:
            self.owned = False
            self.owner = None
            self.owned_num = 0
            self.mortgage = False
            return True
        else:
            return False

    def get_type(self):
        return self.tile_type

    def is_owned(self):
        return self.owned

    def get_owner(self):
        return self.owner

    def get_num_of_color(self):
        return self.num_of_color

    def get_price(self):
        return self.price