from random import choice
from copy import copy

EMPTY_GRID = [[" ", " ", " "] for _ in range(3)]


class User:

    def __init__(self, sign, grid):
        self.name = None
        self.sign = sign
        self.grid = grid
        self.opponent_sign = "O" if self.sign == "X" else "X"

    def occupy_cell(self, row, column):
        self.grid[row][column] = self.sign

    def make_move(self):
        try:
            row, column = [int(x) - 1 for x in
                           input("Enter the coordinates: ").split()]
            assert self.grid[row][column] == " "
            if any([row < 0, row > 2, column < 0, column > 2]):
                raise IndexError

        except ValueError:
            print("You should enter numbers from 1 to 3!")
            return self.make_move()

        except IndexError:
            print("Coordinates should be from 1 to 3!")
            return self.make_move()

        except AssertionError:
            print("This cell is occupied! Choose another one!")
            return self.make_move()

        else:
            self.occupy_cell(row, column)

    def get_winner(self) -> str:
        if [self.sign] * 3 in (
                self.grid[0], self.grid[1], self.grid[2],  # all three rows
                [self.grid[0][0], self.grid[1][0], self.grid[2][0]],  # left column
                [self.grid[0][1], self.grid[1][1], self.grid[2][1]],  # middle column
                [self.grid[0][2], self.grid[1][2], self.grid[2][2]],  # right column
                [self.grid[0][2], self.grid[1][1], self.grid[2][0]],  # main diagonal
                [self.grid[0][0], self.grid[1][1], self.grid[2][2]],  # second diagonal
        ):
            return self.sign

        elif not bool(sum((self.grid[0].count(" "), self.grid[1].count(" "),
                           self.grid[2].count(" ")))):
            return "Draw"

    def print_grid(self):
        print("-" * 9)
        for i in range(len(self.grid)):
            row = "| "
            for j in range(len(self.grid)):
                row += f"{self.grid[i][j]} "
            row += "|"
            print(row)
        print("-" * 9)


class Easy(User):

    def __init__(self, sign, grid):
        super().__init__(sign, grid)
        self.name = "easy"
        self.sign = sign

    def make_move(self):
        # empty (row, column) tuples in a list
        move = [(i, j) for i in range(3) for j in range(3) if self.grid[i][j] == " "]
        random_move = choice(move)  # choose random tuple from list
        self.occupy_cell(*random_move)  # unpack tuple


class Medium(Easy):

    def __init__(self, sign, grid):
        super().__init__(sign, grid)
        self.name = "medium"
        self.sign = sign

    def scan_diagonals(self) -> tuple:
        diagonals = (
            ((0, 0), (1, 1), (2, 2)),
            ((0, 2), (1, 1), (2, 0))
        )

        for diagonal in diagonals:
            # list of symbols at row c[0], column c[1] for row, column in tuples
            diagonal_symbols = [self.grid[c[0]][c[1]] for c in diagonal]
            if any([diagonal_symbols.count(self.sign) == 2,
                    diagonal_symbols.count(self.opponent_sign) == 2]) and " " in diagonal_symbols:
                empty_cell = diagonal_symbols.index(" ")  # index of empty cell
                return diagonal[empty_cell]
        return tuple()

    def make_move(self):
        if self.grid == EMPTY_GRID:
            return super().make_move()

        step = self.scan_diagonals()

        if step == tuple():
            columns = tuple(zip(self.grid[0], self.grid[1], self.grid[2]))
            # i - column number; self.grid[i].index(" ") - index of column in row i
            for i in range(3):
                # row win or block
                if any([self.grid[i].count(self.sign) == 2,
                        self.grid[i].count(self.opponent_sign) == 2]) and " " in self.grid[i]:
                    step = (i, self.grid[i].index(" "))

                # column win or block
                elif any([columns[i].count(self.sign) == 2,
                          columns[i].count(self.opponent_sign) == 2]) and " " in columns[i]:
                    step = (columns[i].index(" "), i)
                if step:
                    break

        if step:
            self.occupy_cell(*step)
        else:
            super().make_move()


class Hard(Medium):

    def __init__(self, sign, grid):
        super().__init__(sign, grid)
        self.name = "hard"
        self.sign = sign

    def minimax(self, depth):
        move_scores = dict()

        fake_board = copy(self.grid)
        simulated_player1, simulated_player2 =\
            Hard(self.sign, fake_board), Hard(self.opponent_sign, fake_board)

        # -10 removed here
        scores = {self.sign: 10, "Draw": 0}

        current_player = simulated_player1
        empty_cells_coordinates = [(i, j) for i in range(3) for j in range(3) if self.grid[i][j] == " "]

        for move in empty_cells_coordinates:
            current_player.occupy_cell(*move)
            winner = self.get_winner()
            if winner:
                move_scores[move] = (scores[winner], depth)
            else:
                current_player = simulated_player2 if current_player == simulated_player1 else simulated_player1
                depth += 1
                current_player.make_move(depth)

        # sorting putting highest score and lowest depth first
        move_scores = dict(sorted(move_scores.items(), key=lambda x: (x[1][0], -x[1][1]), reverse=True))
        return list(move_scores)[0]

    def make_move(self, depth=0):
        if self.grid == EMPTY_GRID:
            return super().make_move()

        # choosing the best move
        best_move = self.minimax(depth)
        return self.occupy_cell(*best_move)
