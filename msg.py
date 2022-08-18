import itertools
import os


class MSG:

    @staticmethod
    def prepare_board_to_show(player):
        return itertools.zip_longest(player.board['1'] or [0, 0, 0], player.board['2'] or [0, 0, 0],
                                     player.board['3'] or [0, 0, 0])

    def single_display_board(self, player):
        player_cols = self.prepare_board_to_show(player)
        print('\n=====================')
        print(f'{player.name} board')
        print('=====================')
        print(f'   Score   ')
        print(f' {player.score["1"]} ', f' {player.score["2"]} ', f' {player.score["3"]} ')
        for a, b, c in player_cols:
            a = a if a is not None else 0
            b = b if b is not None else 0
            c = c if c is not None else 0
            print(f'|{a}|', f'|{b}|', f'|{c}|')

        print(f'Your total score is: {player.total_score}')

    def display_board(self, player, opponent):

        for p in (player, opponent):
            self.single_display_board(p)

    @staticmethod
    def clear_console():
        os.system('clear')

    @staticmethod
    def dice_result(dice_n: int) -> None:
        print(f'Dice Result is ---> {dice_n}')
        print(f'----------------------------------------')

    @staticmethod
    def select_correct_column_number(selected_position: str):
        print('-----------------------------------------------------------------------')
        print(f'You select {selected_position}, pleas select number between 1 and 3')
        print('-----------------------------------------------------------------------')


    @staticmethod
    def column_is_full():
        print('You cant add the number in that row because is full, try in other.')

    @staticmethod
    def player_is_your_turn(player):
        print(f'\n----------------------------------------')
        print(f'{player.name} is your turn')

