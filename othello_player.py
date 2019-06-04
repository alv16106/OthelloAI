import utils
import copy
import numpy as np

def min_max(board, depth, player, maxim):
  if depth == 0 or utils.lastMove(board, player):
    return utils.score(board, player)
  valid = utils.get_moves(board, player)
  if maxim:
    bestValue = -99999
    for move in valid:
      (tmp_board, tot) = utils.move(move, player, copy.deepcopy(board))
      v = min_max(tmp_board, depth - 1, utils.opponent(player), False)
      bestValue = max(bestValue, v)
    # print(np.array(tmp_board).reshape((8,8)))
    return bestValue
  else: # minimizingPlayer
    bestValue = 99999
    for move in valid:
      (tmp_board, tot) = utils.move(move, player, copy.deepcopy(board))
      v = min_max(tmp_board, depth - 1, utils.opponent(player), True)
      bestValue = min(bestValue, v)
    # print(np.array(tmp_board).reshape((8,8)))
    return bestValue

def alpha_beta(board, depth, player, alpha, beta, maxim):
  if depth == 0 or utils.lastMove(board, player):
    return utils.score(board, player), -1
  valid = utils.get_moves(board, player)
  if maxim:
    v = -99999
    for move in valid:
      (tmp_board, tot) = utils.move(move%8, int(move/8), player, copy.deepcopy(board))
      v = max(alpha_beta(tmp_board, depth - 1, utils.opponent(player), alpha, beta, False)[0], v)
      alpha = max(alpha, v)
      if beta <= alpha:
        break
    return v, move
  else: # minimizingPlayer
    v = 99999
    for move in valid:
      (tmp_board, tot) = utils.move(move%8, int(move/8), player, copy.deepcopy(board))
      v = min(alpha_beta(tmp_board, depth - 1, utils.opponent(player), alpha, beta, True)[0], v)
      beta = min(beta, v)
      if beta <= alpha:
        break
    return v, move