# Imports
from dataclasses import dataclass, field
# math
import numpy as np


@dataclass
class Dice:
    number: int = None

    def roll(self) -> None:
        self.number = np.random.randint(1, 7)


@dataclass
class GameBoard:
    board: dict = field(default_factory=dict)
    dice: Dice = field(default_factory=Dice)
    score: dict = field(default_factory=dict)
    total_score: int = 0
    name: str = None

    def set_player_name(self, name: str):
        self.name = name

    def __post_init__(self):
        self.create_new_board()
        self.create_score()

    def __hash__(self):
        return hash(str(self))

    def create_new_board(self) -> None:
        """Create a new empty board game to play"""
        self.board = {'1': list(), '2': list(), '3': list()}

    def create_score(self) -> None:
        """Create a new empty board game to play"""
        self.score = {'1': 0, '2': 0, '3': 0}

    def roll_dice(self):
        """Roll a dice and put the result inside the target colum."""
        return self.dice.roll()

    def add(self, col_number: str, dice_number: int) -> None:
        """Add Dice Result to a Column Board"""
        if not self.is_full(col_number):
            self.board[col_number].append(dice_number)
            print(f'Add {dice_number} value in column {col_number}')

    def remove(self, col_number: str, dice_number: int) -> None:
        """Remove all the same numbers of the column"""
        total_existences = self.count_existences(col_number, dice_number)

        for i in range(total_existences):
            self.board[col_number].remove(dice_number)
            print("Dammmm Son! That's nasty")
            print(f'Remove {total_existences} in the column {col_number}')

    def count_existences(self, col_number: str, dice_number: int) -> int:
        """Check if the number exist in the column"""
        return self.board[col_number].count(dice_number)

    def is_full(self, col_number: str) -> bool:
        """Check if the Column is full. Exist 3 values inside"""
        return len(self.board[col_number]) == 3

    def calculate_col_score(self, col_number: str) -> None:
        """Calculate the score in the column"""

        score_dict = {}
        for n in self.board[col_number]:
            if score_dict.get(n) is None:
                score_dict[n] = 1
            else:
                score_dict[n] += 1

        results = [(count * num) * count for num, count in score_dict.items()]
        self.score[col_number] = sum(results)

    def calculate_total_score(self):
        """Sum all the scores to return a total"""
        self.total_score = sum(self.score.values())
