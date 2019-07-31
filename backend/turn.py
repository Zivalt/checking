class Turn:
    def __init__(self, player="black"):
        self.player = player

    def get_player(self):
        return self.player

    def change_player(self):
        if self.player == "black":
            self.player = "red"
        elif self.player == "red":
            self.player = "black"


