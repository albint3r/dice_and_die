import itertools
import os

class MSG:

    @staticmethod
    def prepare_board_to_show(player, reverse: bool = False):
        zero_lst = [0, 0, 0]
        zip_grid = itertools.zip_longest(player.board['1'] or zero_lst, player.board['2'] or zero_lst,
                                         player.board['3'] or zero_lst,
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

    def single_display_board(self, player, reverse: bool = False):
        player_cols = self.prepare_board_to_show(player, reverse)
        print('\n=====================')
        print(f'{player.name} Board')
        print('=====================')
        print(f'   Score   ')
        print(f' {player.score["1"]} ', f' {player.score["2"]} ', f' {player.score["3"]} ')
        for a, b, c, d in player_cols:
            print(f'|{a}|', f'|{b}|', f'|{c}|')
        print(f'Your total score is: {player.total_score}')

    def display_board(self, player, opponent):

        self.single_display_board(player, True)
        self.single_display_board(opponent, False)

    @staticmethod
    def clear_console():
        os.system('clear')

    @staticmethod
    def dice_result(dice_n: int) -> None:
        print(f'Dice Result is ---> {dice_n}')
        print(f'----------------------------------------\n')

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

    @staticmethod
    def winner_msg(winner, losser):
        print('\n*******************************************')
        print('Game Result:')
        print('*******************************************\n')
        print(f'\nCongratulation {winner.name} you win with [{winner.total_score}] points!!! :)')
        print(f'{losser.name} losse with [{losser.total_score}] points. Losers  go home, bye, bye! ')
        print(f'Game Over!')
