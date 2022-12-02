import re

from players import User, Easy, Medium, Hard

DRAW = "Draw"
MODES = {"user": User,
         "easy": Easy,
         "medium": Medium,
         "hard": Hard}


class TicTacToe:

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.curr_player = player1
        self.winner = None

    def switch_player(self):
        self.curr_player = self.player1 if self.curr_player == self.player2\
            else self.player2

    @classmethod
    def add_players(cls):
        grid = [[" ", " ", " "] for _ in range(3)]

        template = re.compile("exit|start( (user|easy|medium|hard)){2}")
        command = input("Input command: ")

        if not re.match(template, command):
            print("Bad parameters!")
            return TicTacToe.add_players()

        elif command == "exit":
            exit()

        else:
            command = command.split()
            # each player gets assigned their respective sign & grid
            return cls(MODES[command[1]]("X", grid),
                       MODES[command[2]]("O", grid))

    def game_play(self):
        self.player1.print_grid()
        while not self.winner:
            self.curr_player.make_move()
            if self.curr_player.name:
                print(f'Making move level "{self.curr_player.name}"')
            self.curr_player.print_grid()
            self.winner = self.curr_player.get_winner()
            if self.winner:
                print(DRAW if self.winner == DRAW else f"{self.curr_player.sign} wins")
            else:
                self.switch_player()


if __name__ == "__main__":
    game = TicTacToe.add_players()
    game.game_play()
