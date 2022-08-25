# Imports
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
# Regular expression
import random
import pygame
import time
# Project Import
from game.board import GameBoard
from game.msg import MSG
from game.scoreboard import ScoreBoard


@dataclass
class _GameAbstractBase(ABC):
    """ """
    p1: GameBoard = field(default_factory=GameBoard)
    p2: GameBoard = field(default_factory=GameBoard)
    msg: MSG = field(default_factory=MSG)
    selected_position: str = None
    scoreboard: ScoreBoard = field(default_factory=ScoreBoard)

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

    def play_destroy_dice_sound(self, other_player, col_number, dice_number) -> None:
        """Play destroy dice sound N times, this depends on the number of dices destroyed."""
        sound = pygame.mixer.Sound(other_player.dice.destroy_dices_sound)
        for i in range(other_player.count_existences(col_number, dice_number)):
            pygame.mixer.Sound.play(sound)
            time.sleep(.3)

    def check_val_in_opponent_board(self, player: GameBoard, sound_effect = False) -> None:
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
            if sound_effect:
                self.play_destroy_dice_sound(other_player, self.selected_position, player.dice.number)
            other_player.remove(self.selected_position, player.dice.number)
            self.update_score(other_player)

    def change_players_turns(self, player: GameBoard) -> None:
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

        player.is_turn = False
        other_player.is_turn = True

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

    def select_player_start_first(self) -> tuple:
        """Select a random number if is zero player 1 start, but if is two player 2 start """
        rando_n = random.randint(0, 1)
        if rando_n == 0:
            self.p1.is_turn = True
            return self.p1, self.p2
        if rando_n == 1:
            self.p2.is_turn = True
            return self.p2, self.p1

    @abstractmethod
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
        pass

    @abstractmethod
    def show_current_boards(self) -> None:
        """Display the Representation of the boar in the terminal

        Returns
        -------
        None
        """
        pass

    @abstractmethod
    def set_players_names(self):
        """Set the names of the player"""
        pass

    @abstractmethod
    def play(self, echo=False) -> None:
        """Star game play"""
        pass
