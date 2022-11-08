from logic import Game

while True:
    game = Game()
    winner = None
    print('Let the games begin!')

    # start a match
    while winner is None:
        # select gobbler
        print(game.represent_board())
        while winner is None:
            text = f'Player {game.current_player}, select a gobbler to move (1-6): '
            selected_gobbler_size = input(text)
            success = game.select_gobbler(game.current_player, selected_gobbler_size)
            if success:
                break
            else:
                print(('Try again!'))

        # play gobbler
        print(game.represent_board())
        while winner is None:
            text = f'Player {game.current_player}, where would you '\
                f'like to place gobbler {selected_gobbler_size} (1-9)? '
            board_position = input(text)
            success, winner = game.place_selected_gobbler(board_position)
            if success:
                break
            else:
                print('Try again!')

    # announce winner
    print(game.represent_board())
    print(f'Player {winner} has won!')

    # play again?
    play_again = input('Play again? (y/n): ')
    if play_again != 'y':
        break


