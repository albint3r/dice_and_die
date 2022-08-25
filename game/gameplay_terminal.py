# Imports
# Regular expression
import re
import pygame
# Project Import
from game.board import GameBoard
from game._base_gameplay import _GameAbstractBase


class GameTerminal(_GameAbstractBase):
    """ """



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
                if player.is_full(self.selected_position):
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
                if self.is_game_end(player):
                    match_on = False
                    break  # -> This break the for loop no the while loop

        winner, loser = self.select_winner()
        try:
            self.scoreboard.save_match_result(self.p1, self.p2)
            self.msg.winner_msg(winner, loser)
        except AttributeError:
            print('This game wont be saved because is a tie')


class Game2D(_GameAbstractBase):
    pygame.init()
    WIDTH, HEIGHT = 1200, 1000
    BACKGROUND_COLOR = (41, 52, 98)  # White
    LINE_COLOR = (214, 28, 78)
    BOX_COLOR = (220, 220, 220)
    LINE_WIDTH = 15
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Dice And Die Classic')

    def draw_sections(self):
        grid_div = self.WIDTH / 3
        pygame.draw.line(self.WIN, self.BOX_COLOR, (grid_div, 0), (grid_div, self.HEIGHT), 7)
        pygame.draw.line(self.WIN, self.BOX_COLOR, (grid_div * 2, 0), (grid_div * 2, self.HEIGHT), 7)

    def points_box(self):
        """This method display the Box Points of the game result"""
        dimension = (405, 0, 391, 60)  # left, top, width, height
        pygame.draw.rect(self.WIN, self.BOX_COLOR, pygame.Rect(dimension))

    def draw_board_p1(self):
        """Draw the Grid Board Lines"""
        # Vertical Lines
        pygame.draw.line(self.WIN, self.LINE_COLOR, (530, 100), (530, 500), self.LINE_WIDTH)
        pygame.draw.line(self.WIN, self.LINE_COLOR, (660, 100), (660, 500), self.LINE_WIDTH)
        # Horizontal Lines
        pygame.draw.line(self.WIN, self.LINE_COLOR, (410, 230), (790, 230), self.LINE_WIDTH)
        pygame.draw.line(self.WIN, self.LINE_COLOR, (410, 360), (790, 360), self.LINE_WIDTH)

    def draw_board_p2(self):
        """Draw the Grid Board Lines"""
        # Vertical Lines

        pygame.draw.line(self.WIN, self.LINE_COLOR, (530, 560), (530, 960), self.LINE_WIDTH)
        pygame.draw.line(self.WIN, self.LINE_COLOR, (660, 560), (660, 960), self.LINE_WIDTH)
        # Horizontal Lines
        pygame.draw.line(self.WIN, self.LINE_COLOR, (410, 690), (790, 690), self.LINE_WIDTH)
        pygame.draw.line(self.WIN, self.LINE_COLOR, (410, 820), (790, 820), self.LINE_WIDTH)

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

    def show_current_boards(self) -> None:
        """Display the Representation of the boar in the terminal

        Returns
        -------
        None
        """
        pass

    def play(self, echo=False) -> None:
        """Star game play"""
        match_on = True

        self.WIN.fill(self.BACKGROUND_COLOR)
        self.points_box()
        # self.draw_sections()
        self.draw_board_p1()
        self.draw_board_p2()

        # All the logic game need to be inside this while loop
        while match_on:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    match_on = False

            pygame.display.update()

        pygame.quit()
