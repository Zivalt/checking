class Turn:
    def __init__(self, player="X"):
        self.player = player

    def get_player(self):
        return self.player

    def change_player(self):
        if self.player == "X":
            self.player = "O"
        elif self.player == "O":
            self.player = "X"


