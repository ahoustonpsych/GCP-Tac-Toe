from enum import Enum
from flask import Flask, abort, redirect, request, session, url_for
import random
import sys
app = Flask(__name__)
app.debug = True

class Players(Enum):
    X = 'X'
    Y = 'Y'

class Game:
    def __init__(self, SIZE=3):
        self.SIZE = SIZE
        # init board to SIZExSIZE array of None (default 3x3)
        self.BOARD = [] + [[None]*3 for x in range(0, self.SIZE)]
        # player vars
        self.players = Players
        # starting player (random player in Players enum [X or Y])
        self.TURN = [player.value for player in self.players][random.randrange(len(self.players))]
    
    #TODO get board state
    def get_board(self):
        return self.BOARD
    
    #TODO check win condition for @player
    def check_win(self, player):
        return player == winner
    
    #TODO check tie condition (full board)
    def check_tie(self):
        return False

    def move(self, player, moveX, moveY):
        if self.BOARD[moveX][moveY]:
            return 'space occupied'

        self.BOARD[moveX][moveY] = player

        # switch turns!
        self.TURN = 'Y' if self.TURN == 'X' else 'X'
        return self.BOARD

GAME = Game()

@app.route('/')
def landing_page():
    return 'Hello, Toe!'

@app.route('/game')
def show_game():
    return GAME.get_board()

"""
Attempt to make a move for @player at BOARD[moveX][moveY]

Arguments:
    @player: player to make move, 'X' or 'Y'
    @moveX: x position on the board (BOARD[x][])
    @moveY: y position on the board (BOARD[][y])

Return
    @err: error indicating invalid inputs
    @result: new game board
"""
@app.route('/move/<player>/<moveX>/<moveY>', methods=['GET','POST'])
def move(player=None, moveX=None, moveY=None):
    # validate input args
    valid, msg = validate_args(player, moveX, moveY)
    if not valid:
        return msg
    
    # attempt to make move
    err, result, winFlag, tieFlag = GAME.move(player, moveX, moveY)
    if err:
        return err
    elif winFlag:
        return winFlag
    elif tieFlag:
        return tieFlag
    else:
        return GAME.get_board()

# returns if input args are valid, aborts otherwise
# does not check whether or not it's a valid move on the board
def validate_args(player, moveX, moveY):
    # err if player doesn't exist
    if not isinstance(player, str):
        return False,'<b>**ERROR**</b> invalid input for variable <u>"player"</u>. must be <b>X</b> or <b>Y</b>'

    # err if move coords don't exist
    try:
        moveX = int(moveX)
        moveY = int(moveY)
        print(type(moveX),type(moveY))
    except ValueError:
        return False,'<b>**ERROR**</b> invalid move coordinates. <b>0 <= moveX,moveY <= BOARD size</b> (%d)' % len(GAME.BOARD)
    
    # err if move is out of bounds
    # TODO: integrate into Game.move()
    if moveX not in range(GAME.SIZE) or moveY not in range(GAME.SIZE):
        return False,'<b>**ERROR**</b> invalid move coordinates. <b>0 <= moveX,moveY <= BOARD size</b> (%d)' % len(GAME.BOARD)

    return True,(player, int(moveX), int(moveY))
