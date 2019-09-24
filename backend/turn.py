class Turn:
    def __init__(self, player, eat_turn):
        self.player = player
        self.eat_turn = eat_turn

    def get_player(self):
        return self.player

    def set_player(self,player):
        self.player = player

    def change_player(self):
        if self.player == "black":
            self.player = "red"
        elif self.player == "red":
            self.player = "black"

    def get_eat_turn(self):
        return self.eat_turn

    def set_eat_turn(self, flag):
        self.eat_turn = flag
