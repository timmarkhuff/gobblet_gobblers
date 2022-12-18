import  os
import pandas as pd
from matplotlib import pyplot as plt

class Game:
    def __init__(self):
        self.player_names = ['player 0', 'player 1']
        self.winner = None

        # create the gobblers
        number_of_gobblers = 6
        self.gobblers = []
        for player in range(2): # number of players
            size = 1
            for gobbler in range(number_of_gobblers):
                gobbler = Gobbler(player, size)
                self.gobblers.append(gobbler)
                size += 1

        # initialize some values
        self.current_player_idx = 0
        self.selected_gobbler = None
        # used for keeping track of gobblers on board
        self.board = [[] for n in range(9)]

        self.winning_combinations = [
            [0,1,2],
            [3,4,5],
            [6,7,8],
            [0,3,6],
            [1,4,7],
            [2,5,8],
            [0,4,8],
            [6,4,2],
        ]

    def select_gobbler(self, gobbler_size: int) -> bool:
        # Don't allow any more plays if the game is over
        if self.winner is not None:
            return False

        # don't allow the player to select a gobbler if one is
        # already selected
        if self.selected_gobbler:
            return False

        # convert to integer and check if the value is valid (between 0 and 5)
        gobbler_idx = self._convert_input(gobbler_size, 0, 5)

        # if the value is invalid, return False
        if gobbler_idx is None:
            return False
        
        # gobblers can only be selected if they are on top
        gobbler = [g for g in self.gobblers if g.player == self.current_player_idx][gobbler_idx]
        if not gobbler.is_on_top:
            return False

        # if no exclusionary conditions are met, select 
        # the indicated gobbler
        self.selected_gobbler = gobbler

        # remove gobbler from its previous position, if it has one
        if self.selected_gobbler.board_position is not None:
            del self.board[self.selected_gobbler.board_position][-1]

        # update the gobbler's board position
        self.selected_gobbler.board_position_previous = self.selected_gobbler.board_position
        self.selected_gobbler.board_position = None

        # update the is_on_top flag for all gobblers
        self._update_on_top()

        return True

    def place_selected_gobbler(self, board_position: int) -> bool:
        # if there is no selected gobbler, then there is
        # nothing to place
        if not self.selected_gobbler:
            return False, None

        # convert to integer and check if the value is valid (between 0 and 8)
        board_position = self._convert_input(board_position, 0, 8)

        # don't allow the player to put the gobbler back where they got it
        if self.selected_gobbler.board_position_previous == board_position:
            return False, None

        # if the value is invalid, return False
        if board_position is None:
            return False, None

        # if there is already a gobbler on the indicated board
        # position, and it is bigger than the selected gobbler,
        # cannot place the selected gobbler
        if self.board[board_position] and \
            self.selected_gobbler.size <= self.board[board_position][-1].size:
            return False, None

        # add the gobbler to the board
        self.board[board_position].append(self.selected_gobbler)

        # update the gobbler's board position
        self.selected_gobbler.board_position = board_position

        # update the is_on_top flag for all gobblers
        self._update_on_top()
        
        # toggle the current player
        self.current_player_idx = int(not self.current_player_idx)

        # deselect gobbler
        self.selected_gobbler = None

        return True, self._check_for_winner()

    def set_player_names(self, player_names: list) -> list[bool, str]:
        player_name_0 = player_names[0]
        player_name_1 = player_names[1]    
        name_len_requirement = 3
        if len(player_name_0) < name_len_requirement or len(player_name_1) < name_len_requirement:
            return False, f'Player names must be at least {name_len_requirement} characters long.'
        elif player_name_0 == player_name_1:
            return False, 'Player names cannot be identical.'
        else:
            self.player_names = player_names
            return True, 'Let the games begin!'

    def represent_board(self) -> str:
        """
        returns a string representation of the board
        used for playing the game
        """
        str_repr = ''
        n = 0
        for cell in self.board:
            if cell:
                player = cell[-1].player
                size = cell[-1].size
                str_to_add = f'|{size}({player})' 
            else:
                str_to_add = f'|____'
            str_repr += str_to_add

            n += 1

            if n > 2:
                str_repr += '|\n'
                n = 0
        str_repr += '-----------------------'
        return str_repr

    def _convert_input(self, value: int, minimum: int, maximum: int) -> int:
        """
        validates and converts user input into correct data type
        if the value is invalid, returns None
        value: the user-provided value
        minimum: the expected minimum value
        maximum: the expected maximum value
        """
        # convert to an integer
        try:
            value = int(value)
        except ValueError:
            return None

        # convert from a 1-x range to a 0-x range
        value = value - 1 

        # check if the value is within the acceptable range
        if minimum <= value <= maximum:
            return value 
        else:
            return None

    def _check_for_winner(self) -> int:
        """
        checks if there is a winner
        if so, returns winner (int)
        if not, returns None
        """
        # check all of the winning combinations for a winner
        for combo in self.winning_combinations:
            # initialize a list to keep track of the
            # owner of each piece
            result_to_check = []
            for position in combo:
                if self.board[position]: 
                    # record the player of the current piece in a list
                    result_to_check.append(self.board[position][-1].player)
                else:
                    result_to_check.append(None)
            # if there is only one non-None unique value, then
            # we have a winner
            unique_values = list(set(result_to_check))
            if len(unique_values) == 1 and unique_values[0] is not None:
                self.winner = unique_values[0]
                return self.winner
        
        return None
    
    def _update_on_top(self):
        """
        checks all of the gobblers on the board and 
        updates their is_on_top flag
        """
        for position in self.board:
            for n, gobbler in enumerate(position):
                if len(position) - 1 == n:
                    gobbler.is_on_top = True
                else:
                    gobbler.is_on_top = False
    @property
    def winner_name(self) -> str:
        if self.winner is None:
            return None
        else:
            return self.player_names[self.winner]

    @property
    def current_player_name(self) -> str:
        return self.player_names[self.current_player_idx]
     
class Gobbler:
    def __init__(self, player: int, size: int):
        self.player = player # integer 0-1
        self.size = size # integers 0-5
        self.board_position = None # integers 0-8 or None
        self.board_position_previous = None # so that it can be placed back where it came from
        self.is_on_top = True

class GameStats:
    def __init__(self):
        self.num_turns = 0
        self.player = 0
        self.moves = [[],  # a list of lists, one for each player
                      [],]

    def record_move(self, gobbler_size:int, board_position:int) -> None:
        self.moves[self.player].append(f'{gobbler_size} to {board_position}')
        self.num_turns = len(self.moves[0])
        self.player = int(not self.player)

    def save(self, winner) -> None:
        """
        Save the stats to csv and
        save some images.
        """
        self.write_to_csv(winner)
        self.read_stats_from_csv()
        self._save_charts()

    def write_to_csv(self, winner) -> None:
        data_to_record = {
            'winner': winner,
            'first_move_0': self.moves[0][0],
            'first_move_1': self.moves[1][0],
            'last_move_0': self.moves[0][-1],
            'last_move_1': self.moves[1][-1],
            'first_move_winner': self.moves[winner][0],
            'last_move_winner': self.moves[winner][-1],
            'num_turns': self.num_turns,
        }

        path = 'stats.csv'
        column_headers = ''
        line_to_write = ''
        file_is_new = not os.path.exists(path)
        for k, v in data_to_record.items():
            if file_is_new:
                column_headers += f'{k},'

            line_to_write += f'{v},'

        # add linebreaks
        column_headers += '\n'
        line_to_write += '\n'

        # write the column headers
        if file_is_new:
            with open(path, 'a') as f:
                f.write(column_headers)

        # write the line
        with open(path, 'a') as f:
            f.write(line_to_write)

    def read_stats_from_csv(self) -> pd.DataFrame:
        self.stats = pd.read_csv('stats.csv')
        return self.stats

    def _save_charts(self) -> None:
        """
        saves all of the bar charts
        """

        chart_funcs = [self._get_winner_bar_chart,
                    self._get_num_turns_chart,
                    self._get_successful_opening_moves_bar_chart]

        for func in chart_funcs:
            func()

    def _get_winner_bar_chart(self) -> None:
        """
        Given the stats of all previously recorded games,
        generate a bar chart that shows the winner breakdown
        """
        value_counts = self.stats['winner'].value_counts()
        try:
            won_by_0 = value_counts[0]
        except:
            won_by_0 = 0
        try:
            won_by_1 = value_counts[1]
        except:
            won_by_1 = 0
        players = ['Player 0', 'Player 1']
        values = [won_by_0, won_by_1]
        plt.figure(figsize = (4, 4))
        plt.bar(players, values, color=[(0,0,1), (1,191/255,0)], width = 0.3)
        plt.title('Win Count')
        plt.savefig('static/winners.png')

    def _get_successful_opening_moves_bar_chart(self) -> None:
        """
        Given the stats of all previously recorded games,
        generate a bar chart that shows successful opening moves
        """
        value_counts = self.stats['first_move_winner'].value_counts().to_dict()
        moves = list(value_counts.keys())
        counts = list(value_counts.values())
        if len(moves) > 5:
            moves = moves[:5]
            counts = counts[:5]
        plt.figure(figsize = (4, 4))
        plt.bar(moves, counts, color='maroon', width = 0.3)
        plt.title('Successful Openers (Gobbler -> Board Pos.)',)
        plt.savefig('static/opening_moves.png')

    def _get_num_turns_chart(self) -> None:
        """
        Given the stats of all previously recorded games,
        generate a line graph of the number of turns per game
        """
        turns = self.stats['num_turns'].to_list()
        plt.figure(figsize = (4, 4))
        plt.plot(turns, color='blue')
        plt.title('Num. of Turns Each Game',)
        plt.savefig('static/num_turns.png')