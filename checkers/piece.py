import pygame
from .constants import SQUARE_SIZE, CROWN


class Piece:
    # Stores all the data about a single piece
    # Including it's place on the board at all time, and if it's a king or not
    GAP = 10
    OUTLINE = 2

    def __init__(self, row, col, color):
    # Makes a new piece. variables:
    # row, col - which row or col is the piece on
    # color - the color of the piece, red or white
    #isking - is the piece a king or not
    # x,y - the position of the piece on the board
        self.row = row
        self.col = col
        self.color = color
        self.isking = False
        self.x = 0
        self.y = 0
        self.find_pos()

    def find_pos(self):
        # Find the middle of the cube that the piece needs to be on
        # In order to locate it there
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def turn_into_king(self):
        # Turns the piece into a king
        self.isking = True

    def draw_piece(self, win):
    # draws the piece, as a larger circle and a small one on it
    #draw.circle(the window, the color, the place , and the radius)
        radius = SQUARE_SIZE//2 - self.GAP
        pygame.draw.circle(win, self.color, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.isking:
        # if the piece is a king, draw the crown(blit - draw on the front of the screen) on the piece
        # can't be drawn in the (x,y) because it will move, so it will be in the middle of the piece
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))

    def move(self, row, col):
    # Updates the new col and row of the piece, and than the middle of that cube
        self.col = col
        self.row = row
        self.find_pos()

