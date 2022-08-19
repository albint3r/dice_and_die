# Imports
from dataclasses import dataclass, field
# math
import random


@dataclass
class Dice:
    """Represent the Dice of the Game"""
    number: int = None

    def roll(self) -> None:
        """Roll the dice and add the result to the number attribute."""
        self.number = random.randint(1, 6)


@dataclass
class GameBoard:
    """Represent the board game or player"""
    board: dict = field(default_factory=dict)
    dice: Dice = field(default_factory=Dice)
    score: dict = field(default_factory=dict)
    total_score: int = 0
    name: str = None
    winner: bool = None

    def __post_init__(self):
        self.create_new_board()
        self.create_scores()

    def __hash__(self):
        return hash(str(self))

    def set_player_name(self, name: str) -> None:
        """Add the name of the player to the Name attribute

        Parameters
        ----------
        name: str :
            String with the name of the player

        Returns
        -------
        None
        """
        self.name = name

    def create_new_board(self) -> None:
        """Create a new empty board game to play"""
        self.board = {'1': list(), '2': list(), '3': list()}

    def create_scores(self) -> None:
        """Create a new empty board game to play"""
        self.score = {'1': 0, '2': 0, '3': 0}

    def roll_dice(self):
        """Roll a dice and put the result inside the target colum."""
        return self.dice.roll()

    def add(self, col_number: str, dice_number: int) -> None:
        """Add Dice Result to a Column Board

        Parameters
        ----------
        col_number: str :
            Is the Number of the Column position (1, 2 or 3).
        dice_number: int :
            Is the dice roll result.

        Returns
        -------
        None
        """
        if not self.is_full(col_number):
            self.board[col_number].append(dice_number)

    def remove(self, col_number: str, dice_number: int) -> None:
        """Remove all the same numbers of the column

        Parameters
        ----------
        col_number: str :
            Is the Number of the Column position (1, 2 or 3).
        dice_number: int :
            Is the dice roll result.

        Returns
        -------
        None
        """
        total_existences = self.count_existences(col_number, dice_number)

        for i in range(total_existences):
            self.board[col_number].remove(dice_number)
            print("Dammmm Son! That's nasty")

    def count_existences(self, col_number: str, dice_number: int) -> int:
        """Check if the number exist in the column

        Parameters
        ----------
        col_number: str :
            Is the Number of the Column position (1, 2 or 3).
        dice_number: int :
            Is the dice roll result.

        Returns
        -------
        Int
        """
        return self.board[col_number].count(dice_number)

    def is_full(self, col_number: str) -> bool:
        """Check if the Column is full. Exist 3 values inside

        Parameters
        ----------
         col_number: str :
            Is the Number of the Column position (1, 2 or 3).

        Returns
        -------
        Bool
        """
        return len(self.board[col_number]) == 3

    def calculate_col_score(self, col_number: str) -> None:
        """Calculate the score in the column

        Parameters
        ----------
        col_number: str :
            Is the Number of the Column position (1, 2 or 3).

        Returns
        -------
        None
        """

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

    def is_grid_full(self):
        """Check if the grid is full. If is true the game is ended"""
        return sum([len(col) for col in self.board.values()]) == 9

