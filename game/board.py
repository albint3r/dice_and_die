# Imports
import pygame
from dataclasses import dataclass, field
# math
import random
import os
import itertools


@dataclass
class Dice:
    """Represent the Dice of the Game"""

    _max_dice_numbers: int = 6
    number: int = None
    size: tuple[int, int] = (100, 100)
    is_num: bool = False
    number_surf: pygame.Surface = None
    number_rect: pygame.Rect = None
    shadow_rect: pygame.Rect = None
    souffle_dice_sound: str = None
    throw_dice_sound: str = None
    destroy_dices_sound: str = None

    def __post_init__(self):
        self.set_dice_sounds()

    def roll(self, fake_roll: bool = False) -> None:
        """Roll the dice and add the result to the number attribute.
        Also fill the 'fake_roll' attribute tha works with the 2D version game, to make the shuffle dice effect.

        Parameters:
        -------------
        fake_roll: bool
            This switch activate the Fake roll effect when the user is going to throw the dice.
            If this is False it would save the dice roll result, otherwise only would help to print result in the
            game.
            (Default = False)
        """
        self.number = random.randint(1, self._max_dice_numbers)
        if not fake_roll:
            self.is_num = True

    def set_dice_sounds(self) -> None:
        """Add the directory path to the variables that handle the Dice Sound"""
        self.souffle_dice_sound = os.path.join('game', 'sounds', 'dice', 'dice_shaking_effect.mp3')
        self.throw_dice_sound = os.path.join('game', 'sounds', 'dice', 'throw_dice_effect.mp3')
        self.destroy_dices_sound = os.path.join('game', 'sounds', 'dice', 'destroy_dices_effect.mp3')

    def create_dice_img(self, screen: pygame.Surface, turn: int, blit: bool = False) -> None:
        """Create the dice image of the player in the board game. This Method creates two objects the square of the
        dice and the number inside the dice.

        Parameters:
        -------------
        screen: pygame.Surface:
            Is the game main display screen object. This helps to display the square and the number of the dice.

        turn: int:
            This number represent the players turn. If is 0 is turn of the player1 elif 1 is turn of the player2

        blit: bool
            If this is true it would display the dice new number.
            (Default: False)
        """

        # Create Font
        font = pygame.font.Font(None, 80)
        self.number_surf = font.render(f'{self.number}', True, 'Black')
        # Create Dice Square
        self.number_rect = pygame.Rect((0, 0), self.size)  # 100 x 100 square
        self.shadow_rect = pygame.Rect((0, 0), self.size)
        # Select in the MIDTOP coordinates of the number and shadow rect.
        if turn == 0:  # Player1
            self.number_rect.midtop = (1000, 200)
            self.shadow_rect.midtop = (980, 210)
            dice_num_coordinates = (985, 225)
        elif turn == 1:  # Player2
            self.number_rect.midtop = (200, 700)
            self.shadow_rect.midtop = (180, 710)
            dice_num_coordinates = (185, 725)

        if blit:  # Display the new dice number
            pygame.draw.rect(screen, 'Black', self.shadow_rect)
            pygame.draw.rect(screen, 'White', self.number_rect)
            # Display Number
            screen.blit(self.number_surf, dice_num_coordinates)


@dataclass
class GameBoard:
    """Represent the board game or player"""
    board: dict = field(default_factory=dict)
    dice: Dice = field(default_factory=Dice)
    score: dict = field(default_factory=dict)
    total_score: int = 0
    per_total_score: float = 0
    name: str = None
    winner: bool = None
    board_surf: pygame.Surface = None
    board_rect: pygame.Rect = None
    slash_surf: pygame.Surface = None
    slash_rect: pygame.Rect = None
    is_turn: bool = False

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
        self.name = name.title()

    def create_new_board(self) -> None:
        """Create a new empty board game to play"""
        self.board = {'1': list(), '2': list(), '3': list()}

    def get_board_img(self) -> str:
        return os.path.join('game', 'statics', 'board', 'board_grid.png')

    def create_d2_board(self, is_player1=True):
        self.board_surf = pygame.image.load(self.get_board_img())
        if is_player1:
            self.board_rect = self.board_surf.get_rect(midtop=(600, 100))
        else:
            self.board_rect = self.board_surf.get_rect(midtop=(600, 600))

    def create_arrow_turn_indicator(self, screen, is_player1=False):
        """Create an arrow to display in the Dashboard to indicate is the turn of the player"""
        if is_player1:
            pygame.draw.polygon(surface=screen, color=(255, 0, 0), points=[(1000, 350), (950, 400), (1050, 400)])
        else:
            pygame.draw.polygon(surface=screen, color=(255, 0, 0), points=[(200, 850), (150, 900), (250, 900)])

    def create_slash_destroy_img(self, is_player1: bool = True):
        """Create the slash image that would be displayed when the player destroy the dices of the opponent"""
        img_file = os.path.join('game', 'statics', 'board', 'slash_dice_destroy.png')
        picture = pygame.image.load(img_file)
        self.slash_surf = pygame.transform.scale(picture, (600, 600))
        if is_player1:
            self.slash_rect = self.slash_surf.get_rect(midtop=(600, 50))

        else:
            self.slash_rect = self.slash_surf.get_rect(midtop=(600, 500))

    def create_scores(self) -> None:
        """Create a new empty board game to play"""
        self.score = {'1': 0, '2': 0, '3': 0}

    def roll_dice(self, fake_roll=False):
        """Roll a dice and put the result inside the target colum."""
        return self.dice.roll(fake_roll)

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
        if not self.is_col_full(col_number):
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

    def count_existences(self, col_number: str, dice_number: int) -> int:
        """Count how many occurrences of the number exist

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

    def is_col_full(self, col_number: str) -> bool:
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

    @staticmethod
    def prepare_board_to_show(player, reverse: bool = False) -> zip:
        zero_lst = [0, 0, 0]

        zip_grid = itertools.zip_longest(player.board['1'], player.board['2'],
                                         player.board['3'],
                                         zero_lst  # This additional Column is hidden, It works to display the 3 row.
                                         , fillvalue=0)

        if reverse:
            col1, col2, col3, col4 = [], [], [], []

            for a, b, c, d, in zip_grid:
                col1.append(a)
                col2.append(b)
                col3.append(c)
                col4.append(d)

            zip_grid = zip(col1[::-1], col2[::-1], col3[::-1], col4[::-1])

        return zip_grid
