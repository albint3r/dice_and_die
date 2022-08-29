from game.gameplay_terminal import GameTerminal
from game.gamplay2d import Game2D
from game.board import GameBoard

def play():
    game = Game2D()
    game.p1.name = 't'
    game.p2.name = 'b 3'
    game.play()


if __name__ == '__main__':
    play()
