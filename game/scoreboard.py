# Import
from dataclasses import dataclass, field
import json
import datetime as dt


@dataclass
class ScoreBoard:
    score_story: list = field(default_factory=list)
    score_story_root_path = str = 'score_story.js'

    def load(self) -> None:
        with open(self.score_story_root_path) as file:
            self.score_story = json.load(file)

    def insert_game_result(self, player1, player2) -> None:
        result_game = {'date': dt.datetime.utcnow(), 'player1': player1.name, 'player2': player2.name,
                       'winner': player1.name if player1.winner is True else player2.name,
                       'losser': player1.name if player1.winner is not True else player2.name,
                       'w_score': player1.total_score if player1.winner is True else player2.total_score,
                       'l_score': player1.total_score if player1.winner is not True else player2.total_score}

        self.score_story.append(result_game)

    def save(self) -> None:
        jsonfile = json.dumps(self.score_story, default=str)
        with open(self.score_story_root_path, 'w') as file:
            file.write(jsonfile)

    def save_match_result(self, player1, player2):
        self.load()
        self.insert_game_result(player1, player2)
        self.save()
