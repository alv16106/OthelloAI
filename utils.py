import time
import copy
N = 8
DIR = [1,-1,8,-8,9,-9,7,-7]
dirx = [-1, 0, 1, -1, 1, -1, 0, 1]
diry = [-1, -1, -1, 0, 0, 1, 1, 1]

def opponent(player):
  return 1 if player is 2 else 2

def move(x, y, player, board):
  totctr = 0 # total number of opponent pieces taken
  board[N*y + x] = player
  for d in range(8): # 8 directions
    ctr = 0
    for i in range(N):
      dx = x + dirx[d] * (i + 1)
      dy = y + diry[d] * (i + 1)
      if dx < 0 or dx > N - 1 or dy < 0 or dy > N - 1:
        ctr = 0; break
      elif board[dy*N + dx] == player:
        break
      elif board[dy*N + dx] == 0:
        ctr = 0; break
      else:
        ctr += 1
    for i in range(ctr):
      dx = x + dirx[d] * (i + 1)
      dy = y + diry[d] * (i + 1)
      board[dy*N + dx] = player
    totctr += ctr
  return (board, totctr)


# Que movimientos podemos hacer?
def get_moves(board, player):
  validMoves = []
  for i, piece in enumerate(board):
    if not piece:
      (tmp_board, tot) = move(i%N, int(i/N), player, copy.deepcopy(board))
      """ for movement in DIR:
        valid = False
        d = i + movement
        row = int(d/N)
        col = d%N
        if row < 0 or row > N - 1 or col < 0 or col > N - 1 or d < 0:
          continue
        elif board[d] == player:
          continue
        elif board[d] == 0:
          continue
        else:
          valid = True
        valid and i not in validMoves and validMoves.append(i) """
      tot and i not in validMoves and validMoves.append(i)
  return validMoves

# Aplicar movimoento a un board
def make_move(move, player, board):
  board[move] = player
  for d in DIR:
    make_flips(move, player, board, d)
  return board

def make_flips(move, player, board, direction):
  bracket = find_bracket(move, player, board, direction)
  if not bracket:
    return
  square = move + direction
  while square != bracket:
    board[square] = player
    square += direction

def find_bracket(square, player, board, direction):
  bracket = square + direction
  row = int(bracket/N)
  col = bracket%N
  if row < 0 or row > N - 1 or col < 0 or col > N - 1 or bracket < 0 or bracket > 63:
    return None
  if board[bracket] == player:
    return None
  opp = opponent(player)
  while board[bracket] == opp:
    bracket += direction
  row = int(bracket/N)
  col = bracket%N
  if row < 0 or row > N - 1 or col < 0 or col > N - 1 or bracket < 0:
    return None
  return bracket

# Heuristica a utilizar (esquinas valen mas aparentemente?)
def score(board, player):
  tot = 0
  for i, piece in enumerate(board):
    if piece == player:
      row = int(i/N)
      col = i%N
      if (row == 0 or row == N - 1) and (col == 0 or col == N - 1):
        tot += 4 # corner
      elif (row == 0 or row == N- 1) or (col == 0 or col == N - 1):
        tot += 2 # side
      else:
        tot += 1
  return tot

def lastMove(board, player):
  return not len(get_moves(board, player))
