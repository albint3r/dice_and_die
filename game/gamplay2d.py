# Imports
# Regular expression
import re
import pygame
# Project Import
from game.board import GameBoard
from game.scoreboard import ScoreBoard
from game._base_gameplay import _GameAbstractBase
from game.msg import MSG


class Game2D(_GameAbstractBase):
    WIDTH, HEIGHT = 1200, 1000
    BACKGROUND_COLOR = '#122339'  # DarkBlue
    FPS = 60

    def __init__(self):
        self.p1 = GameBoard()
        self.p2 = GameBoard()
        self.msg = MSG()
        self.scoreboard = ScoreBoard()
        self.first_turn = True
        self.turn_n = 1
        self.total_points_game = 0

        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.font = pygame.font.Font(None, 30)
        pygame.display.set_caption('Dice And Die Classic')
        self.p1.create_d2_board()
        self.p2.create_d2_board(False)

    def set_players_names(self):
        """Set the names of the player"""
        pass

    def create_mid_line_div(self):
        """Create a middle line division"""
        pygame.draw.line(self.screen, 'White', (0, 500), (1200, 500), 10)

    def select_dice_position(self, player: GameBoard, event) -> None:
        """Select the Column position to put the dice result (1, 2 or 3)

        Parameters
        ----------
        player: GameBoard :
            Is the GameBoard object or Player


        Returns
        -------
        None
        """
        # Player Select Column
        if event.key == pygame.K_1 and player.dice.is_num and self.selected_position is None:
            self.selected_position = '1'
            print(f'Select {self.selected_position}')

        if event.key == pygame.K_2 and player.dice.is_num and self.selected_position is None:
            self.selected_position = '2'
            print(f'Select {self.selected_position}')

        if event.key == pygame.K_3 and player.dice.is_num and self.selected_position is None:
            self.selected_position = '3'
            print(f'Select {self.selected_position}')

        if self.selected_position is not None:
            if player.is_col_full(self.selected_position):
                self.selected_position = None
                print('Is full the Column')

    def show_current_scores(self):
        p1 = self.p1
        p2 = self.p2

        # if p1.score_surf is None and p1.score_rect is None:
        score_surf_p1 = self.font.render(
            f'{p1.score["1"]}                {p1.score["2"]}               {p1.score["3"]}',
            False, 'White')

        score_surf_p2 = self.font.render(
            f'{p2.score["1"]}                {p2.score["2"]}               {p2.score["3"]}',
            False, 'White')
        # score_rect = score_surf.get_rect(topleft=(485, 55))
        self.screen.blit(score_surf_p1, (485, 55))
        self.screen.blit(score_surf_p2, (485, 940))

    def show_current_turn(self):
        font = pygame.font.Font(None, 90)
        turn = font.render(f"Turno : {self.turn_n} ", True, (0, 0, 0))
        box_turn = pygame.Rect((450, 464), (350, 75))
        box_turn.midtop = (600, 464)
        pygame.draw.rect(self.screen, 'White', box_turn)
        self.screen.blit(turn, (455, 472))

    def show_players_total_scores(self):
        font = pygame.font.Font(None, 50)
        total_score_p1 = font.render(f'{self.p1.total_score}', True, 'Black')
        total_score_p2 = font.render(f'{self.p2.total_score}', True, 'Black')
        self.screen.blit(total_score_p1, (435, 10))
        self.screen.blit(total_score_p2, (735, 10))

    def show_players_names(self):
        white_bg = 'white'
        font = pygame.font.Font(None, 50)
        total_score_p1 = font.render(f'{self.p1.name}', True, white_bg)
        total_score_p2 = font.render(f'{self.p2.name}', True, white_bg)
        self.screen.blit(total_score_p1, (50, 10))
        self.screen.blit(total_score_p2, (1000, 10))

    def show_current_boards(self, zip_grid, blit=False, player1=True) -> None:
        """Display the Representation of the boar in the terminal

        Returns
        -------
        None
        """

        font = pygame.font.Font(None, 40)

        board_grid = [font.render(f'{a}          {b}           {c}', True, (255, 255, 255)) for a, b, c, d in zip_grid]

        if blit:
            if player1:
                row1, row2, row3 = 150, 245, 345
                self.screen.blit(board_grid[0], (495, row1))
                self.screen.blit(board_grid[1], (495, row2))
                self.screen.blit(board_grid[2], (495, row3))
            else:
                row1, row2, row3 = 650, 745, 845
                self.screen.blit(board_grid[0], (495, row1))
                self.screen.blit(board_grid[1], (495, row2))
                self.screen.blit(board_grid[2], (495, row3))

    def set_total_points(self):
        """Get the sum of the score of the players 1 and 2"""
        self.total_points_game = self.p1.total_score + self.p2.total_score

    def set_calculate_percentage_of_total_score_players(self) -> None:
        """This function calculate the percentage of p1 and p2 from the total points game """
        if self.p1.total_score:
            self.p1.per_total_score = self.p1.total_score / self.total_points_game
        if self.p2.total_score:
            self.p2.per_total_score = self.p2.total_score / self.total_points_game

    def show_bar_score_points(self):
        self.set_total_points()
        self.set_calculate_percentage_of_total_score_players()
        self.scoreboard.create_sentiment_score_bar(self.p1, self.p2, self.screen)

    def play(self, echo=False) -> None:
        """Star game play"""
        game_on = True

        players = self.select_player_start_first()
        turn = 0

        while game_on:
            self.screen.fill(self.BACKGROUND_COLOR)
            self.create_mid_line_div()
            self.screen.blit(self.p1.board_surf, self.p1.board_rect)
            self.screen.blit(self.p2.board_surf, self.p2.board_rect)
            self.scoreboard.create_score_box(self.screen)
            # Todo New working area
            self.show_bar_score_points()
            #############################################
            # If dice image exist display value
            if self.p1.dice.number_rect is not None:

                if self.p1.is_turn:  # Turn player 1
                    self.p1.create_arrow_turn_indicator(self.screen, True)

                self.p1.dice.create_dice_img(self.screen, 0, True)
                zip_grid = self.p1.prepare_board_to_show(self.p1, True)
                self.show_current_boards(zip_grid, True)
            if self.p2.dice.number_rect is not None:  # Turn player 2

                if self.p2.is_turn:
                    self.p2.create_arrow_turn_indicator(self.screen, False)

                self.p2.dice.create_dice_img(self.screen, 1, True)
                zip_grid = self.p2.prepare_board_to_show(self.p2, False)
                self.show_current_boards(zip_grid, True, player1=False)

            # 1- Event
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()

                # Player roll dice
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not players[turn].dice.is_num:
                        players[turn].roll_dice()
                        players[turn].dice.create_dice_img(self.screen, turn, False)
                        print(f'Turno {turn}')
                        print(f'is Turno {players[turn].is_turn}')
                        print(players[turn].name)
                        print(players[turn].dice.number)
                        print('Roll the dice')

                    # Player Select Column
                    self.select_dice_position(players[turn], event)
                    if self.selected_position is not None:
                        self.check_val_in_opponent_board(players[turn])
                        self.add_to_board(players[turn])
                        # Update the Grid Values of the Game
                        zip_grid = players[turn].prepare_board_to_show(players[turn], False)
                        self.show_current_boards(zip_grid, False)
                        self.update_score(players[turn])
                        # Reset all the values to chang of player
                        self.selected_position = None
                        players[turn].dice.is_num = False
                        self.turn_n += 1

                        if self.is_game_end(players[turn]):
                            game_on = False

                        if turn == 0:

                            self.change_players_turns(players[turn])
                            turn = 1

                        elif turn == 1:
                            self.change_players_turns(players[turn])
                            turn = 0

            self.show_current_turn()
            self.show_players_total_scores()
            self.show_players_names()
            self.show_current_scores()
            pygame.display.update()

        pygame.quit()

        winner, loser = self.select_winner()

        try:
            self.scoreboard.save_match_result(self.p1, self.p2)
            self.msg.winner_msg(winner, loser)

        except AttributeError:
            print('This game wont be saved because is a tie')

