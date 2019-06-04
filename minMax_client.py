import socketio
import othello_player
import random as r
import utils
import copy
import numpy as np


HOST = 'http://192.168.1.148:4000';
tileRep = ['_', 'X', 'O']
N = 8
userName = 'Rodrigo Alvarado'
tournamentID = 142857;

sio = socketio.Client()
sio.connect(HOST)

@sio.on('connect')
def on_connect():
  print('conectado')
  sio.emit('signin', {'user_name': userName, 'tournament_id': tournamentID, 'user_role': 'player'})

@sio.on('ready')
def on_ready(data):
  print('ready')
  best = 0
  bm = 0
  validMoves = utils.get_moves(data['board'], data['player_turn_id'])
  print(validMoves)
  print(np.array(data['board']).reshape((8,8)))
  value, move = othello_player.alpha_beta(data['board'], 4, data['player_turn_id'], -99999, 99999, True)
  print(np.array(data['board']).reshape((8,8)))
  print(bm)
  sio.emit('play', {
    'player_turn_id': data['player_turn_id'],
    'tournament_id': tournamentID,
    'game_id': data['game_id'],
    'movement': move,
  })

@sio.on('finish')
def on_finish(data):
  print('Juego terminado')
  sio.emit('player_ready', {
    'tournament_id': tournamentID,
    'game_id': data['game_id'],
    'player_turn_id': data['player_turn_id']
  })