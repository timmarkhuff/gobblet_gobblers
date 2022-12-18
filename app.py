from flask import Flask, render_template, request, redirect
from logic import Game, GameStats

app = Flask(__name__)
game = Game()
game_stats = GameStats()

@app.route("/play", methods=['POST','GET'])
def play():
    global game

    # make a play
    message = None
    play_button_pressed = ('Play' in request.form.getlist('button'))
    if request.method == 'POST' and play_button_pressed:
        selected_gobbler = request.form['gobbler_size']
        board_position = request.form['board_position']
        select_success = game.select_gobbler(selected_gobbler)
        place_success, winner = game.place_selected_gobbler(board_position)
        
        if not select_success or not place_success:
            message = 'Invalid selection!'   
        else:
            game_stats.record_move(selected_gobbler, board_position)

        if winner is not None:
            game_stats.save(winner)

    # start a new game
    new_game_button_pressed = ('New Game' in request.form.getlist('button')) 
    if request.method == 'POST' and new_game_button_pressed:
        return redirect('/')

    # view stats
    stats_button_pressed = ('View Stats' in request.form.getlist('button')) 
    if request.method == 'POST' and stats_button_pressed:
        return redirect('/stats')

    return render_template('play.html', game=game, message=message)
    

@app.route("/", methods=['POST','GET'])
def index():
    global game
    button_pressed = ('Start Game' in request.form.getlist('button'))
    if request.method == 'POST' and button_pressed:
        player_names = request.form.getlist('name')
        success, response = game.set_player_names(player_names)
        if success:
            return redirect('/play')
    elif request.method == 'GET':
        # start a new game when the index page is loaded
        game = Game() 
    return render_template('index.html')

@app.route("/stats", methods=['POST','GET'])
def stats():
    global game_stats
    new_game_button_pressed = ('New Game' in request.form.getlist('button'))
    if request.method == 'POST' and new_game_button_pressed:
        return redirect('/')
    return render_template('stats.html')

if __name__ == "__main__":
    app.run(debug=True, port=8000)