# Imports
# Regular expression
import re
# Project Import
from game.board import GameBoard
from game._base_gameplay import _GameAbstractBase


class GameTerminal(_GameAbstractBase):
    """ """

    def __init__(self):
        super().__init__()
        self.turn_n = 1

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
            self.selected_position = input(f'\n[{player.name}] you get [{player.dice.number}]. Select Column to insert '
                                           f'Dice:')
            if bool(re.search(PATTERN, self.selected_position)) and int(self.selected_position) < 4:
                if player.is_col_full(self.selected_position):
                    self.msg.column_is_full()
                else:
                    break
            else:
                self.msg.select_correct_column_number(self.selected_position)

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

    def set_players_names(self):
        """Set the names of the player"""
        name_p1 = input('Player 1 Select your name: ')
        name_p2 = input('Player 2 Select your name: ')
        self.p1.set_player_name(name_p1)
        self.p2.set_player_name(name_p2)

    def play(self, echo=False) -> None:
        """Star game play"""
        self.set_players_names()
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
                if not echo:
                    # Print all the changes if this is True
                    self.msg.clear_console()
                # Count Turns
                self.turn_n += 1
                if self.is_game_end(player):
                    match_on = False
                    break  # -> This break the for loop no the while loop

        winner, loser = self.select_winner()
        try:
            self.scoreboard.save_match_result(self.p1, self.p2, self.turn_n)
            self.msg.winner_msg(winner, loser)
        except AttributeError:
            print('This game wont be saved because is a tie')
