import  os
import pandas as pd

class Game:
    def __init__(self):
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
        self.current_player = 0
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
        gobbler = [g for g in self.gobblers if g.player == self.current_player][gobbler_idx]
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
        self.current_player = int(not self.current_player)

        # deselect gobbler
        self.selected_gobbler = None

        return True, self._check_for_winner()

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
                return unique_values[0]
        
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
        return pd.read_csv('stats.csv')

