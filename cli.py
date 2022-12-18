from logic import Game
import random

class Player:
    def __init__(self, player_number, name, game):
        self.player_number = player_number
        self.name = name
        self.repr = f'{name}({player_number})'
        self.game = game

class Human(Player):
    def __init__(self, player_number, name, game):
        super().__init__(player_number, name, game)

    def select_gobbler(self):
        text = f'{self.repr}, select a gobbler to move (1-6): '
        return input(text)

    def select_board_position(self):
        text = f'{self.repr}, where would you '\
                f'like to place gobbler {self.game.selected_gobbler.size} (1-9)? '
        return input(text)

class Bot(Player):
    def __init__(self, player_number, name, game):
        super().__init__(player_number, name, game)

    def select_gobbler(self):
        available_gobblers = [g for g in self.game.gobblers if g.player == self.player_number and g.is_on_top]
        random_idx = random.randint(0, len(available_gobblers) - 1)
        return available_gobblers[random_idx].size

    def select_board_position(self):
        return random.randint(0, 9)

while True:
    game = Game()
    winner = None
    print('Let the games begin!')

    # create players
    players = []
    for player_number in range(2):
        txt = f'Enter a name for player {player_number}. Leave blank to make it a bot: '
        name = input(txt)
        if name:
            players.append(Human(player_number, name, game))
        else:
            players.append(Bot(player_number, 'Bot', game))

    # start a match
    while winner is None:
        # select gobbler
        current_player = players[game.current_player_idx]
        print(game.represent_board())

        while winner is None:
            selected_gobbler_size = current_player.select_gobbler()
            success = game.select_gobbler(selected_gobbler_size)
            if success:
                print(f'{current_player.repr} selects gobbler {selected_gobbler_size}.')
                break
            else:
                print(('Try again!'))

        # play gobbler
        print(game.represent_board())
        while winner is None:
            board_position = current_player.select_board_position()
            success, winner = game.place_selected_gobbler(board_position)
            if success:
                print(f'{current_player.repr} moves gobbler {selected_gobbler_size} to {board_position}.')
                break
            else:
                print('Try again!')

    # announce winner
    print(game.represent_board())
    winner = players[winner]
    print(f'{winner.repr} has won!')

    # play again?
    play_again = input('Play again? (y/n): ')
    if play_again != 'y':
        break

print('Thank you for playing.')


