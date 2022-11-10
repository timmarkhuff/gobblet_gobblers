import cv2
import numpy as np
from math import sqrt
from logic import Game

class Board:
    def __init__(self, game):
        self.game = game

        self.winner = None
        self.blue = (255,0,0)
        self.orange = (0,191,255)
        self.hover_coordinate_x = 0
        self.hover_coordinate_y = 0

        # board dimensions
        self.main_area_width = 500
        self.main_area_height = 500
        self.margin_width = 140

        # construct the blank board
        overall_dimensions = (self.main_area_height, self.main_area_width + 2 * self.margin_width)
        self.blank_board = np.zeros(overall_dimensions, dtype='uint8')
        self.blank_board.fill(200)
        self.blank_board = cv2.cvtColor(self.blank_board, cv2.COLOR_GRAY2BGR)

        # draw the lines (horizontal)
        x1 = self.margin_width
        x2 = self.main_area_width + self.margin_width
        y = 0
        for _ in range(2):
            y += self.main_area_height/3
            cv2.line(self.blank_board, (x1, round(y)), (x2, round(y)), (0,255,0), 6)
        
        # draw the lines (vertical)
        x = self.margin_width
        y1 = 0
        y2 = self.main_area_height
        for _ in range(4):
            cv2.line(self.blank_board, (round(x), y1), (round(x), y2), (0,0,255), 6)
            x += self.main_area_width / 3

        self.static_board = self.blank_board.copy()

        # gobbler parameters
        self.max_gobbler_radius = 42
        self.min_gobbler_radius = 25
        self.gobbler_radius_range = self.max_gobbler_radius - self.min_gobbler_radius

        # add some display parameters to gobblers
        player_0_x = self.margin_width / 2
        player_1_x = self.margin_width * 1.5 + self.main_area_width
        for gobbler in self.game.gobblers:
            # assign colors and x coordinates (which
            # are dependent on team)
            if gobbler.player == 0:
                gobbler.color = self.blue
                gobbler.x = player_0_x
            else:
                gobbler.color = self.orange
                gobbler.x = player_1_x
            # assign y coordinates and radius (which
            # are dependent on gobbler size)
            gobbler.y = (gobbler.size - 1) * self.main_area_height / 6  \
                        + self.main_area_height / 12
            gobbler.radius = (gobbler.size - 1) * self.gobbler_radius_range / 6  \
                        + self.min_gobbler_radius

    def draw_static_board(self) -> np.ndarray: 
        self.static_board = self.blank_board.copy()
        gobblers_sorted = sorted(self.game.gobblers, key=lambda x: x.size, reverse=False)
        for gobbler in gobblers_sorted:
            center = (round(gobbler.x), round(gobbler.y))
            radius = round(gobbler.radius)
            color = gobbler.color
            if gobbler is not self.game.selected_gobbler:
                cv2.circle(self.static_board, center, radius, color, -1) 
                text = str(gobbler.size)
                pos = (round(gobbler.x - 6), round(gobbler.y + 4))
                cv2.putText(self.static_board, text, pos, cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,(255,255,255), 1, cv2.LINE_AA)    
        self.dynamic_board = self.static_board.copy()     

    def draw_dynamic_board(self):
        self.dynamic_board = self.static_board.copy()
        gobbler = self.game.selected_gobbler
        radius = round(gobbler.radius * 1.2)

        # draw a transparent shadow
        overlay = self.static_board.copy()
        center = (round(gobbler.x), round(gobbler.y))
        shadow = (0,0,0)
        cv2.circle(overlay, center, radius, shadow, -1)
        self.dynamic_board = cv2.addWeighted(self.dynamic_board, .9, overlay, .1, 0)

        # draw the selected gobbler
        offset = 8
        offset_center = (round(gobbler.x + offset), round(gobbler.y - offset))
        color = gobbler.color
        white = (255,255,255)
        cv2.circle(self.dynamic_board, offset_center, radius, color, -1) 
        cv2.circle(self.dynamic_board, offset_center, radius, white, 2) 

        # put text on the gobbler
        text = str(gobbler.size)
        pos = (round(gobbler.x - 6 + offset), round(gobbler.y + 4 - offset))
        cv2.putText(self.dynamic_board, text, pos, cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, white, 1, cv2.LINE_AA)

    def draw_cursor(self):
        # copy the static board to get a fresh copy to draw on
        self.dynamic_board = self.static_board.copy()

        # determine the color of the player
        if self.game.current_player == 0:
            color = self.blue
        else:
            color = self.orange

        # define the lines of the crosshairs
        x = self.hover_coordinate_x
        y = self.hover_coordinate_y
        cursor_width = 20
        cursor_thickness = 6
        pt1_hor = (x - cursor_width, y)
        pt2_hor = (x + cursor_width, y)
        pt1_vert = (x, y - cursor_width)
        pt2_vert = (x, y + cursor_width)

        # white background lines
        border_thickness = 3
        cv2.line(self.dynamic_board, pt1_hor, pt2_hor, (255,255,255), cursor_thickness + border_thickness)
        cv2.line(self.dynamic_board, pt1_vert, pt2_vert, (255,255,255), cursor_thickness + border_thickness)
        # colored foreground lines
        cv2.line(self.dynamic_board, pt1_hor, pt2_hor, color, cursor_thickness)
        cv2.line(self.dynamic_board, pt1_vert, pt2_vert, color, cursor_thickness)

    def draw_winner(self):
        x1 = self.margin_width + self.main_area_width / 6
        y1 = self.main_area_height / 5
        pt1 = (round(x1), round(y1))
        x2 = self.margin_width + self.main_area_width - self.main_area_width / 6
        y2 = y1 + 100
        pt2 = (round(x2), round(y2))
        cv2.rectangle(self.dynamic_board, pt1, pt2, (110,110,110), -1)
        cv2.rectangle(self.dynamic_board, pt1, pt2, (0,0,0), 2)

        if self.winner == 0:
            color = self.blue
        else:
            color = self.orange

        text = f'Player {self.winner} is the winner!'
        cv2.putText(self.dynamic_board, text, (round(x1 + 34), round(y1 + 35)), cv2.FONT_HERSHEY_COMPLEX_SMALL, .75, color, 1, cv2.LINE_AA)
        text = 'Press any key to continue.'
        cv2.putText(self.dynamic_board, text, (round(x1 + 34), round(y1 + 65)), cv2.FONT_HERSHEY_COMPLEX_SMALL, .75, color, 1, cv2.LINE_AA)

    def click_event(self, event, x, y, flags, param):
        """
        Callback function used by the main loop to track clicks
        and hovering.
        """
        self.hover_coordinate_x, self.hover_coordinate_y = x, y

        if event == cv2.EVENT_LBUTTONDOWN:
            if self.game.selected_gobbler is None:
                clicked_gobbler = self.check_for_clicked_gobbler(x, y)
                if clicked_gobbler:
                    self.game.select_gobbler(clicked_gobbler)
                    self.draw_static_board()
            else:
                clicked_region = self.check_board_region(x, y)
                if clicked_region:
                    gobbler = self.game.selected_gobbler
                    success, self.winner = self.game.place_selected_gobbler(clicked_region)
                    if success:
                        self.place_gobbler_on_board(gobbler, clicked_region)
                        self.draw_static_board()

    def check_for_clicked_gobbler(self, x, y):
        """
        Given x and y coorindates, return the size (1-6) of 
        the gobbler that was clicked.
        Return None if no gobbler was clicked.
        """
        # get a list of the current player's gobblers
        current_players_gobblers = [g for g in self.game.gobblers if g.player == self.game.current_player]
        # sort them such that the bigger gobblers are listed first
        # this is to ensure that they are selected when a gobbler of a smaller size
        # and same player is present beneath
        current_players_gobblers = sorted(current_players_gobblers, key = lambda x: x.size, reverse=True)
        for gobbler in current_players_gobblers:
            a = x - gobbler.x
            b = y - gobbler.y
            distance = sqrt(a ** 2 + b ** 2)
            if distance <= gobbler.radius:
                return gobbler.size
        return None

    def check_board_region(self, x, y):
        """
        Given an x and y coordinate, return the coresponding board 
        region (1-9).
        Return None if the coordinate is not on a board region, e.g.
        on the sideline
        """
        y_start = 0
        y_end = y_start + self.main_area_height / 3
        region = 1
        for column in range(3):
            x_start = self.margin_width
            x_end = x_start + self.main_area_width / 3
            for row in range(3):
                if x_start < x <= x_end and y_start < y <= y_end:
                    return region
                region += 1
                x_start += self.main_area_width / 3
                x_end += self.main_area_width / 3

            y_start += self.main_area_height / 3
            y_end += self.main_area_height / 3
        return None

    def place_gobbler_on_board(self, gobbler, provided_region):
        """
        Update the x and y coordinate of a gobbler such that it
        lies in the center of the provided board region
        """
        y = self.main_area_height / 6
        region = 1
        for column in range(3):
            x = self.margin_width + self.main_area_width / 6
            for row in range(3):
                if region == provided_region:
                    gobbler.x = x
                    gobbler.y = y 
                x += self.main_area_width / 3
                region += 1
            y += self.main_area_height / 3


def main():
    board = Board(Game())
    # board.game.selected_gobbler = board.game.gobblers[8]
    board.draw_static_board()

    while True:
        # update the cooridinates of the selected gobbler
        if board.game.selected_gobbler is not None:
            board.game.selected_gobbler.x = board.hover_coordinate_x
            board.game.selected_gobbler.y = board.hover_coordinate_y
            board.draw_dynamic_board()
        else:
            board.draw_cursor()
        if board.winner is not None:
            board.draw_static_board()
            board.draw_winner()
            cv2.imshow('Gobblet Gobblers', board.dynamic_board)
            cv2.waitKey(0)
            board = Board(Game())
            board.draw_static_board()

        cv2.imshow('Gobblet Gobblers', board.dynamic_board)
        cv2.setMouseCallback("Gobblet Gobblers", board.click_event)

        key = cv2.waitKey(30)
        if key == ord('q'):
            break
    
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()