"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    xs = 0
    os = 0
    for row in board:
        for cell in row:
            if cell == X:
                xs += 1
            elif cell == O:
                os += 1
    return X if xs == os else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_set = set()
    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            if cell == EMPTY:
                actions_set.add((r, c))
    return actions_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    possible_actions = actions(board)
    current_player = player(board)

    if action not in possible_actions:
        raise Exception('Not valid action')
    
    new_board = [row.copy() for row in board]
    new_board[action[0]][action[1]] = current_player
    return new_board


def row_win(board, p):
    win_cond = []
    for row in board:
        win_cond.append(all([c == p for c in row]))
    return any(win_cond)


def column_win(board, p):
    win_cond = []
    for c in range(3):
        win_cond.append(all([board[r][c] == p for r in range(3)]))
    return any(win_cond)


def diag_win(board, p):
    win_cond = []
    win_cond.append(all([board[c][c] == p for c in range(3)]))
    win_cond.append(all([board[c][2 - c] == p for c in range(3)]))
    return any(win_cond)


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if any([row_win(board, X), column_win(board, X), diag_win(board, X)]):
        return X
    elif any([row_win(board, O), column_win(board, O), diag_win(board, O)]):
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) in (X, O) or not actions(board)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    if w == X:
        return 1
    elif w == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    def find_next_move(current_board):
        if terminal(current_board):
            return (None, utility(current_board))
        minmax = min if player(current_board) == O else max
        pos_sol = [].copy()
        acts = actions(current_board)
        for action in acts:
            pos_sol.append((action, find_next_move(result(current_board, action))[1]))
        if len(pos_sol) == 1:
            return pos_sol[0]
        return minmax(*pos_sol, key=lambda x: x[1])
    return find_next_move(board)[0]
