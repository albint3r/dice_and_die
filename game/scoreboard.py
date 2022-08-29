# Import
from dataclasses import dataclass, field
import json
import datetime as dt
import pygame


@dataclass
class ScoreBoard:
    POINTS_BOX_SIZE = (350, 30)
    score_story: list = field(default_factory=list)
    score_story_root_path = str = 'score_story.js'
    score_rect = None
    shadow_score_rect = None
    points_p1_rect = None
    points_p2_rect = None

    def load(self) -> None:
        with open(self.score_story_root_path) as file:
            self.score_story = json.load(file)

    def insert_game_result(self, player1, player2, total_turns) -> None:
        result_game = {'date': dt.datetime.utcnow(), 'player1': player1.name, 'player2': player2.name,
                       'winner': player1.name if player1.winner is True else player2.name,
                       'losser': player1.name if player1.winner is not True else player2.name,
                       'w_score': player1.total_score if player1.winner is True else player2.total_score,
                       'l_score': player1.total_score if player1.winner is not True else player2.total_score,
                       'total_turns': total_turns}

        self.score_story.append(result_game)

    def save(self) -> None:
        jsonfile = json.dumps(self.score_story, default=str)
        with open(self.score_story_root_path, 'w') as file:
            file.write(jsonfile)

    def save_match_result(self, player1, player2, total_turns):
        self.load()
        self.insert_game_result(player1, player2, total_turns)
        self.save()

    def create_score_box(self, screen):
        coordinates = (425, 10)
        self.POINTS_BOX_SIZE = (350, 30)
        self.score_rect = pygame.Rect(coordinates, self.POINTS_BOX_SIZE)
        self.shadow_score_rect = pygame.Rect((422, 13), self.POINTS_BOX_SIZE)
        pygame.draw.rect(screen, 'Black', self.shadow_score_rect)
        pygame.draw.rect(screen, 'Red', self.score_rect)

    def create_sentiment_score_bar(self, player1, player2, screen):
        """Create half of the bar in the point bar box to display the sentiment of the match"""
        sentiment_bar_score_coordinate = (425, 10)
        half_bar_size = (175, 30)

        if player1.total_score and player2.total_score:
            # If the two players have total score it would display the sentiment bar
            per_box_points_p1 = round(player1.per_total_score * self.POINTS_BOX_SIZE[0])  # Todo Could be a good idea create a function for this calculus
            point_bar_rect = pygame.Rect(sentiment_bar_score_coordinate, (per_box_points_p1, 30))
            pygame.draw.rect(screen, 'Green', point_bar_rect)
        else:
            # Create half bar to display until points arrive to create calculation.
            point_bar_rect = pygame.Rect(sentiment_bar_score_coordinate, half_bar_size)  # x, y and Width, height
            pygame.draw.rect(screen, 'Green', point_bar_rect)
            # Create text indicator
            font = pygame.font.Font(None, 25)
            text = font.render('Wait for sentiment...', False, 'Black')
            screen.blit(text, (520, 17))

