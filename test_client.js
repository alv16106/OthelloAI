const io = require('socket.io-client');
const HOST = 'http://192.168.1.127:4000';

console.log(io.listen)

const tileRep = ['_', 'X', 'O'],
    N = 8;

function randInt(min, max){
  return parseInt(Math.floor(Math.random()*(max-min+1)+min));
}

const socket = io.connect(HOST),
    userName = 'Rodrigo.amiguito',
    tournamentID = 142857;  

socket.on('connect',function(){

  // Client has connected
  console.log("Conectado: " + userName);

  // Signing signal
  socket.emit('signin', {
    user_name: userName,
    tournament_id: tournamentID,  // 142857
    user_role: 'player'
  });
});

socket.on('ready', function(data){
  console.log('Tiro')

  let posmov = []
  for (let i = 0; i < data.board.length; i++) {
    !data.board[i] && posmov.push(i)
  }

  socket.emit('play', {
    player_turn_id: data.player_turn_id,
    tournament_id: tournamentID,
    game_id: data.game_id,
    movement: posmov[randInt(0, posmov.length)],
  });
});

socket.on('finish', function(data){

  // The game has finished
  console.log("Game " + data.game_id + " has finished");

  // Inform my students that there is no rematch attribute
  console.log("Ready to play again!");

  // Start again!

  socket.emit('player_ready', {
    tournament_id: tournamentID,
    game_id: data.game_id,
    player_turn_id: data.player_turn_id
  });

});