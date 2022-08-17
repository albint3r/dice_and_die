# Imports
from dataclasses import dataclass, field
# Regular expresion
import re
# Project Import
from board import GameBoard


@dataclass
class Game:

    p1: GameBoard = field(default_factory=GameBoard)
    p2: GameBoard = field(default_factory=GameBoard)
    selected_position: str = None

    def __post_init__(self):
        self.set_players_names()

    def set_players_names(self):
        self.p1.name = input('Player 1 Select your name: ')
        self.p2.name = input('Player 2 Select your name: ')

    def is_game_end(self):
        """Check if the game is ended. THis happened when the boar of any player have all columns filled.
        This is a Result of 9"""
        boards = self.p1.board, self.p2.board

        for board in boards:

            p_result = 0

            for column in board.values():
                total_fill_spaces = len(column)
                p_result += total_fill_spaces


            if p_result == 9:
                # print('FIN DEL JUEGO')
                return True
            else:
                # print('EL JUEGO SIGUE')
                return False

    def select_dice_position(self, player) -> None:
        PATTERN = '[0-3]'
        print(f'The Dice Result was ---> {player.dice.number}')
        while True:
            self.selected_position = input(f'Select the Column to put the number: ')
            if re.search(PATTERN, self.selected_position):
                if player.is_full(self.selected_position):
                    print('You cant add the number in that row because is full, try in other.')
                else:
                    break
            else:
                print('-----------------------------------------------------------------------')
                print(f'You select {self.selected_position}, pleas select number between 1 and 3')
                print('-----------------------------------------------------------------------')

    def check_val_in_opponent_board(self, player):
        other_player = {self.p1: self.p2, self.p2: self.p1}.get(player)
        if other_player.count_existences(self.selected_position, player.dice.number) > 0:
            other_player.remove(self.selected_position, player.dice.number)
            self.update_score(other_player)
            print(f'Other Player Score was updates ')

    def add_to_board(self, player):
        player.add(self.selected_position, player.dice.number)

    def show_current_boards(self, player) -> None:
        other_player = {self.p1: self.p2, self.p2: self.p1}.get(player)

        print(f'{player.name} board')
        print('=====================')
        print(player.board)
        print(player.score)
        print(f'Your total score is: {player.total_score}')
        print('\n')
        print(f'{other_player.name} board')
        print('=====================')
        print(other_player.board)
        print(other_player.score)
        print(f'Your total score is: {other_player.total_score}')
        print('\n')

    def update_score(self, player):
        player.calculate_col_score(self.selected_position)
        player.calculate_total_score()

    def select_winner(self):
        if self.p1.total_score > self.p2.total_score:
            return self.p1
        elif self.p2.total_score > self.p2.total_score:
            return self.p2
        else:
            return 'Tie'

    def play(self):
        """Star game play"""

        players = (self.p1, self.p2)

        # Select Player start
        while not self.is_game_end():

            for player in players:
                print(f'\n----------------------------------------')
                print(f'{player.name} is your turn')
                print(f'----------------------------------------')
                player.roll_dice()
                self.show_current_boards(player)
                self.select_dice_position(player)
                self.check_val_in_opponent_board(player)
                self.add_to_board(player)
                self.update_score(player)
                self.show_current_boards(player)

        winner = self.select_winner()
        print(f'Congratulation {winner.name}!!! :)')
