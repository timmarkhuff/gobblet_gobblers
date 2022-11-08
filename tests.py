import unittest
from logic import Game

class TestLogic(unittest.TestCase):

    def test_init(self):
        game = Game()
        self.assertEqual(game.current_player, 0)

    def test_select_gobbler_from_sideline(self):
        game = Game()
        success = game.select_gobbler(game.current_player, 3)
        self.assertEqual(success, True)

    def test_select_gobbler_from_board_success(self):
        game = Game()

        # player 0 plays
        _ = game.select_gobbler(game.current_player, 4)
        _, _ = game.place_selected_gobbler(1)

        # player 1 plays
        _ = game.select_gobbler(game.current_player, 3)
        _, _ = game.place_selected_gobbler(2)

        # player 0 picks up gobbler from board
        success = game.select_gobbler(game.current_player, 4)

        self.assertEqual(success, True)

    def test_select_gobbler_from_board_failure(self):
        game = Game()

        # player 0 plays
        _ = game.select_gobbler(game.current_player, 4)
        _, _ = game.place_selected_gobbler(1)

        # player 1 plays
        _ = game.select_gobbler(game.current_player, 5)
        _, _ = game.place_selected_gobbler(1)

        # player 0 picks up gobbler from board
        success = game.select_gobbler(game.current_player, 4)

        self.assertEqual(success, False)

    def test_place_gobbler_success(self):
        """
        Player picks up a gobbler and puts it down
        on a valid spot.
        """
        game = Game()

        _ = game.select_gobbler(game.current_player, 4)
        success, _ = game.place_selected_gobbler(1)

        self.assertEqual(success, True)

    def test_place_gobbler_failure(self):
        """
        Player picks up a gobbler and attempts
        to place it somewhere that isn't allowed
        """
        game = Game()

        # player 0 plays
        _ = game.select_gobbler(game.current_player, 4)
        _, _ = game.place_selected_gobbler(1)

        # player 1 plays
        _ = game.select_gobbler(game.current_player, 3)
        success, _ = game.place_selected_gobbler(1)

        self.assertEqual(success, False)

    def test_represent_board(self):
        game = Game()
        game.represent_board()

    def test_convert_input_(self):
        game = Game()

        inputs = [
            # user_input, minimum, maximum, expected_result
            [3, 1, 6, 2],
            [10, 1, 6, None],
            ['6', 1, 6, 5],
            ['asdfadsfads', 1, 6, None],
        ]

        for i in inputs:
            user_input = i[0]
            minimum = i[1]
            maximum = i[2]
            expected_result = i[3]
            actual_result = game._convert_input(user_input, minimum, maximum)

            self.assertEqual(expected_result, actual_result)

    def test_check_for_winner_0(self):
        game = Game()

        plays = [
            # selected_gobbler_size, board_position
            [1,1], # player 0
            [1,2], # player 1
            [2,5],
            [2,3],
            [3,9],
        ]
        
        for play in plays:
            selected_gobbler_size = play[0]
            board_position = play[1]
            _ = game.select_gobbler(game.current_player, selected_gobbler_size)
            _, winner = game.place_selected_gobbler(board_position)

        self.assertEqual(winner, 0)

    def test_check_for_winner_1(self):
        game = Game()

        plays = [
            # selected_gobbler_size, board_position
            [1,1], # player 0
            [2,1], # player 1
            [2,2],
            [3,4],
            [5,3],
            [6,8],
            [4,6],
            [6,7],

        ]
        
        for play in plays:
            selected_gobbler_size = play[0]
            board_position = play[1]
            _ = game.select_gobbler(game.current_player, selected_gobbler_size)
            _, winner = game.place_selected_gobbler(board_position)

        self.assertEqual(winner, 1)

    def test_update_on_top(self):
        game = Game()

        # player 0 plays
        _ = game.select_gobbler(game.current_player, 2)
        _, _ = game.place_selected_gobbler(1)

        before = game.board[0][0].is_on_top

        # player 1 plays
        _ = game.select_gobbler(game.current_player, 3)
        _, _ = game.place_selected_gobbler(1)

        after = game.board[0][0].is_on_top

        self.assertEqual((before, after), (True, False))

if __name__ == '__main__':
    unittest.main()