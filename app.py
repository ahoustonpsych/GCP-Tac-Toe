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

    def get_board(self):
        return str(self.BOARD)
    
    #TODO check win condition for @player
    def check_win(self, player):
        return player == winner

    def check_tie(self):
        # return False if any rows have a Nonetype
        return not True in [None in row for row in self.BOARD]
        
        # equiv. to:
        # for row in self.BOARD:
        #    if None in row:
        #        return False
        # return True

    def move(self, player, moveX, moveY):
        if str(player).upper() != self.TURN:
            return 'not your turn', None, None, None

        if self.BOARD[int(moveX)][int(moveY)]:
            return 'space occupied', None, None, None

        # empty space! make the move
        self.BOARD[int(moveX)][int(moveY)] = player
        
        #TODO check win condition
        #if self.check_win(self.TURN):
            #TODO properly end the game
        #    return None, self.BOARD, '<h1><b>%s WON THE GAME</b></h1>' % self.TURN, None
        
        #TODO fix return args
        if self.check_tie():
            return None, self.BOARD, None, "<h2><b>IT'S A DRAW!</b></h2>"

        # switch turns!
        self.TURN = 'Y' if self.TURN == 'X' else 'X'
        # success
        return None, self.BOARD, None, None


GAME = Game()

# generate new board
# TODO integrate into Game class
def new_game():
    GAME = Game()
    return GAME.get_board()

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
    # @get: return current player
    #if request.method == 'GET':
    #    return 'Next player: ' + GAME.TURN
    print('request:', request, request.form)

    # parse POST args
    if request.method == 'POST':
        player = request.form['player']
        moveX = request.form['moveX']
        moveY = request.form['moveY']

    print('raw input args: ', player, moveX, moveY)
    # abort if invalid inputs
    valid, msg = validate_args(player, moveX, moveY)
    if not valid:
        return msg

    print('Validated Inputs:', player, moveX, moveY)
    print(type(player), type(moveX), type(moveY))
    
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
    #if not isinstance(moveX, int) or isinstance(moveY, int):
    #    return False,'<b>**ERROR**</b> invalid move coordinates. <b>0 <= moveX,moveY <= BOARD size</b> (%d)' % len(GAME.BOARD)
    # err if invalid player choice (not X or Y)
    if player.upper() not in [player.value for player in GAME.players]:
        return False,'<b>**ERROR**</b> invalid player value. must be <b>%s</b>' % [player.value for player in GAME.players].join('</b> or <b>') # <b>X</b> or <b>Y</b>'

    # err if move is out of bounds
    # TODO: integrate into Game.move()
    if moveX not in range(GAME.SIZE) or moveY not in range(GAME.SIZE):
        return False,'<b>**ERROR**</b> invalid move coordinates. <b>0 <= moveX,moveY <= BOARD size</b> (%d)' % len(GAME.BOARD)

    return True,(player, int(moveX), int(moveY))
