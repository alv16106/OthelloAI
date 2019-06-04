import socketio
import random as r

HOST = 'http://localhost:4000';
tileRep = ['_', 'X', 'O']
N = 8
userName = 'Rodrigo.random2'
tournamentID = 12;

sio = socketio.Client()
sio.connect(HOST)

@sio.on('connect')
def on_connect():
  print('conectado')
  sio.emit('signin', {'user_name': userName, 'tournament_id': tournamentID, 'user_role': 'player'})

@sio.on('ready')
def on_ready(data):
  print('ready')
  posmov = []
  for i in range(len(data['board'])):
    not data['board'][i] and posmov.append(i)

  sio.emit('play', {
    'player_turn_id': data['player_turn_id'],
    'tournament_id': tournamentID,
    'game_id': data['game_id'],
    'movement': posmov[r.randint(0, len(posmov) - 1)],
  })

@sio.on('finish')
def on_finish(data):
  print('Juego terminado')
  sio.emit('player_ready', {
    'tournament_id': tournamentID,
    'game_id': data['game_id'],
    'player_turn_id': data['player_turn_id']
  })