from monopoly.BuyableLand import BuyableLand


class Service(BuyableLand):
    def __init__(self, service_type):
        super().__init__(150, [4,10], 2, "Service")
        self.service_type = service_type

    def get_rent(self, dice):
        if self.owned_num == self.num_of_color:
            return self.rents[1]*dice
        else:
                return self.rents[0]*dice