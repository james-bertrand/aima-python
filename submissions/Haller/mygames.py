from collections import namedtuple
from games import (Game)
import copy

class GameState:
    def __init__(self, to_move, board, label=None, depth=8):
        self.to_move = to_move
        self.board = board
        self.label = label
        self.maxDepth = depth

    def __str__(self):
        if self.label == None:
            return super(GameState, self).__str__()
        return self.label

class Oink(Game):
    """A flagrant copy of TicTacToe, from game.py
    It's simplified, so that moves and utility are calculated as needed
    Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""

    def __init__(self):
        self.collCount = 4
        self.rowCount = 4
        self.piggyX = 0
        self.piggyY = 1
        self.fencesX = {'F1':3,
                       'F2':3,
                       'F3':3,
                       'F4':3}
        self.fencesY = {'F1':0,
                       'F2':1,
                       'F3':2,
                       'F4':3}
        self.initial = GameState(to_move='P', board=[ [' ','P',' ',' '],
                                                            [' ',' ',' ',' '],
                                                        [' ',' ',' ',' '],
                                                            ['F1','F2','F3','F4']])

    def actions(self, state):
        try:
            return state.moves
        except:
            pass
        "Legal moves are any square not yet taken."
        moves = []
        if state.to_move =='P':
            for i in range(self.rowCount):
                if i % 2 == 0 and 'P' in state.board[i]:
                    loc = state.board[i].index('P')
                    if i-1 >= 0:
                        if state.board[i-1][loc] == ' ':
                            moves.append('P to (' + str(i-1) + ',' + str(loc) + ')')
                        if loc-1 >= 0 and state.board[i-1][loc-1] == ' ':
                            moves.append('P to (' + str(i-1) + ',' + str(loc-1) + ')')
                    if i+1 < self.rowCount:
                        if state.board[i+1][loc] == ' ':
                            moves.append('P to (' + str(i+1) + ',' + str(loc) + ')')
                        if loc-1 >= 0 and state.board[i+1][loc-1] == ' ':
                            moves.append('P to (' + str(i+1) + ',' + str(loc-1) + ')')
                if i % 2 != 0 and 'P' in state.board[i]:
                    loc = state.board[i].index('P')
                    if i-1 >= 0:
                        if state.board[i-1][loc] == ' ':
                            moves.append('P to (' + str(i-1) + ',' + str(loc) + ')')
                        if loc+1 < self.collCount and state.board[i-1][loc+1] == ' ':
                            moves.append('P to (' + str(i-1) + ',' + str(loc+1) + ')')
                    if i+1 < self.rowCount:
                        if state.board[i+1][loc] == ' ':
                            moves.append('P to (' + str(i+1) + ',' + str(loc) + ')')
                        if loc+1 < self.collCount and state.board[i+1][loc+1] == ' ':
                            moves.append('P to (' + str(i+1) + ',' + str(loc+1) + ')')
        if state.to_move =='F':
            for k in self.fencesY.keys():
                for i in range(self.rowCount):
                    if i % 2 == 0 and k in state.board[i]:
                        if i-1 >= 0:
                            if state.board[i-1][self.fencesY[k]] == ' ':
                                moves.append(k + ' to(' + str(i-1) + ',' + str(loc) + ')')
                            if loc-1 >= 0 and state.board[i-1][self.fencesY[k]-1] == ' ':
                                moves.append(k + ' to(' + str(i-1) + ',' + str(loc-1) + ')')
                    if i % 2 != 0 and k in state.board[i]:
                        if i-1 >= 0:
                            if state.board[i-1][self.fencesY[k]] == ' ':
                                moves.append(k + ' to(' + str(i-1) + ',' + str(loc) + ')')
                            if loc+1 < self.collCount and state.board[i-1][self.fencesY[k]+1] == ' ':
                                moves.append(k + ' to(' + str(i-1) + ',' + str(loc+1) + ')')

        state.moves = moves
        return moves

    # defines the order of play
    def opponent(self, player):
        if player == 'P':
            return 'F'
        if player == 'F':
            return 'P'
        return None

    def result(self, state, move):
        if move not in self.actions(state):
            return state  # Illegal move has no effect
        board = copy.deepcopy(state.board)
        if state.to_move == 'P':
            player = 'P'
        else:
            player = move[:2]
        tempX = int(move[6:-3])
        tempY = int(move[8:-1])
        board[tempX][tempY] = player
        if state.to_move == 'P':
            board[self.piggyX][self.piggyY] = ' '
            self.piggyX = tempX
            self.piggyY = tempY
        else:
            board[self.fencesX[player]][self.fencesY[player]] = ' '
            self.fencesX[player] = tempX
            self.fencesY[player] = tempY
        next_mover = self.opponent(player)
        return GameState(to_move=next_mover, board=board)

    def utility(self, state, player):
        "Return the value to player; 1 for win, -1 for loss, 0 otherwise."
        try:
            return state.utility if player == 'P' else -state.utility
        except:
            pass
        board = state.board
        util = self.check_win(board, 'P')
        if util == 0:
            util = -self.check_win(board, 'F')
        state.utility = util
        return util if player == 'P' else -util

    # Did I win?
    def check_win(self, board, player):
        # check rows
        for y in range(1, self.v + 1):
            if self.k_in_row(board, (1,y), player, (1,0)):
                return 1
        # check columns
        for x in range(1, self.h + 1):
            if self.k_in_row(board, (x,1), player, (0,1)):
                return 1
        # check \ diagonal
        if self.k_in_row(board, (1,1), player, (1,1)):
            return 1
        # check / diagonal
        if self.k_in_row(board, (3,1), player, (-1,1)):
            return 1
        return 0

    def terminal_test(self, state):
        "A state is terminal if it is won or there are no empty squares."
        return self.utility(state, 'P') != 0 or len(self.actions(state)) == 0

    def display(self, state):
        board = state.board
        for x in range(self.rowCount):
            for y in range(self.collCount):
                if x % 2 == 0:
                    pStr = board[x][y] + '#'
                if x % 2 != 0:
                    pStr = '#' + board[x][y]
                print(pStr, end='')
            print()


myGame = Oink()

won = GameState(
    to_move = 'O',
    board = {(1,1): 'X', (1,2): 'X', (1,3): 'X',
             (2,1): 'O', (2,2): 'O',
            },
    label = 'won'
)

winin1 = GameState(
    to_move = 'X',
    board = {(1,1): 'X', (1,2): 'X',
             (2,1): 'O', (2,2): 'O',
            },
    label = 'winin1'
)

losein1 = GameState(
    to_move = 'O',
    board = {(1,1): 'X', (1,2): 'X',
             (2,1): 'O', (2,2): 'O',
             (3,1): 'X',
            },
    label = 'losein1'
)

winin3 = GameState(
    to_move = 'X',
    board = {(1,1): 'X', (1,2): 'O',
             (2,1): 'X',
             (3,1): 'O',
            },
    label = 'winin3'
)

losein3 = GameState(
    to_move = 'O',
    board = {(1,1): 'X',
             (2,1): 'X',
             (3,1): 'O', (1,2): 'X', (1,2): 'O',
            },
    label = 'losein3'
)

winin5 = GameState(
    to_move = 'X',
    board = {(1,1): 'X', (1,2): 'O',
             (2,1): 'X',
            },
    label = 'winin5'
)

lost = GameState(
    to_move = 'X',
    board = {(1,1): 'X', (1,2): 'X',
             (2,1): 'O', (2,2): 'O', (2,3): 'O',
             (3,1): 'X'
            },
    label = 'lost'
)

myGames = {
    myGame: [
        won,
        winin1, losein1, winin3, losein3, winin5,
        lost,
    ]
}