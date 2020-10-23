from monopoly.BuyableLand import BuyableLand


class Transport(BuyableLand):
    def __init__(self, transport_num):
        super().__init__(200, [25, 50, 100, 200], 4, "Transport")
        self.transport_num = transport_num

    def get_rent(self):
        return self.rents[self.owned_num]