# Imports
from dataclasses import dataclass, field
# Regular expression
import re
import random
# Project Import
from typing import Tuple
from board import GameBoard
from msg import MSG
from scoreboard import ScoreBoard


@dataclass
class Game:
    """ """
    p1: GameBoard = field(default_factory=GameBoard)
    p2: GameBoard = field(default_factory=GameBoard)
    msg: MSG = field(default_factory=MSG)
    selected_position: str = None
    scoreboard: ScoreBoard = field(default_factory=ScoreBoard)

    def __post_init__(self):
        self.set_players_names()

    def set_players_names(self):
        """Set the names of the player"""
        self.p1.name = input('Player 1 Select your name: ')
        self.p2.name = input('Player 2 Select your name: ')

    def is_game_end(self, player: GameBoard) -> bool:
        """Check if the game is ended. This happened when the boar of any player have all columns filled.
        This is a Result of 9

        Parameters
        ----------
        player: GameBoard :
            Is the GameBoard object or Player

        Returns
        -------
        Bool
        """

        return player.is_grid_full()

    def select_dice_position(self, player: GameBoard) -> None:
        """Select the Column position to put the dice result (1, 2 or 3)

        Parameters
        ----------
        player: GameBoard :
            Is the GameBoard object or Player
            

        Returns
        -------
        None
        """
        PATTERN = '[0-3]'
        while True:
            self.selected_position = input(f'Select the Column to put the number: ')
            if bool(re.search(PATTERN, self.selected_position)) and int(self.selected_position) < 4:
                if player.is_full(self.selected_position):
                    self.msg.column_is_full()
                else:
                    break
            else:
                self.msg.select_correct_column_number(self.selected_position)

    def check_val_in_opponent_board(self, player: GameBoard) -> None:
        """Check if the selection of the current player is in the Opponent player. If is true, it will
        remove all the values equal of the dice result.

        Parameters
        ----------
        player: GameBoard :
            Is the GameBoard object or Player
            

        Returns
        -------
        None
        """
        other_player = {self.p1: self.p2, self.p2: self.p1}.get(player)
        if other_player.count_existences(self.selected_position, player.dice.number) > 0:
            other_player.remove(self.selected_position, player.dice.number)
            self.update_score(other_player)

    def add_to_board(self, player: GameBoard) -> None:
        """Add the Result of the dice to the board in the select column position.

        Parameters
        ----------
        player: GameBoard :
            Is the GameBoard object or Player
            

        Returns
        -------
        None
        """
        player.add(self.selected_position, player.dice.number)

    def show_current_boards(self) -> None:
        """Display the Representation of the boar in the terminal

        Returns
        -------
        None
        """

        # Players 1 and 2
        player1 = self.p1
        player2 = self.p2
        self.msg.display_board(player1, player2)

    def update_score(self, player: GameBoard) -> None:
        """Update the score of the column and the total

        Parameters
        ----------
        player: GameBoard :
            Is the GameBoard object or Player

        Returns
        -------
        None
        """
        player.calculate_col_score(self.selected_position)
        player.calculate_total_score()

    def select_winner(self) -> tuple[GameBoard, GameBoard] | tuple[str, str]:
        """Select the winner of the game by the high score."""
        if self.p1.total_score > self.p2.total_score:
            # Player 1 Win the game
            self.p1.winner = True
            self.p2.winner = False
            return self.p1, self.p2
        elif self.p2.total_score > self.p1.total_score:
            # Player 2 win the game
            self.p2.winner = True
            self.p1.winner = False
            return self.p2, self.p1
        else:
            return 'Nobody win', 'You Guys'

    def select_player_start_first(self):
        """Select a random number if is zero player 1 start, but if is two player 2 start """
        rando_n = random.randint(0, 1)
        return (self.p1, self.p2) if rando_n == 0 else (self.p2, self.p1)

    def play(self, echo=False) -> None:
        """Star game play"""
        match_on = True
        players = self.select_player_start_first()

        # Select Player start
        while match_on:

            for player in players:
                self.msg.player_is_your_turn(player)
                player.roll_dice()
                self.msg.dice_result(player.dice.number)
                self.show_current_boards()
                self.select_dice_position(player)
                self.check_val_in_opponent_board(player)
                self.add_to_board(player)
                self.update_score(player)
                if echo is not False:
                    # Print all the changes if this is True
                    self.msg.clear_console()
                if self.is_game_end(player):
                    match_on = False
                    break  # -> This break the for loop no the while loop

        winner, loser = self.select_winner()
        try:
            self.scoreboard.save_match_result(self.p1, self.p2)
            self.msg.winner_msg(winner, loser)
        except AttributeError:
            print('This game wont be saved because is a tie')
