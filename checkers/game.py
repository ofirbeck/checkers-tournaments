import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from .board import Board


class Game:
    def __init__(self, win, color):
    # Creates the game. variables:
    # selected - which piece is clicked on and chosen
    # board - the board
    # win - the window
    # turn - whose turn it is
    # valid_moves - what moves can be made in the state of the board
        self.selected = None
        self.board = Board()
        self.win = win
        self.turn = color
        self.valid_moves = {}

    def update(self):
    # updates the screen to the new current of the board
        self.board.draw_board(self.win)
        self.draw_vaild_moves(self.valid_moves)
        pygame.display.update()

    def reset(self):
    # restart all variables in order to start a new game
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}
        self.update()

    def select(self, row , col):
    # Selects a piece that was clicked on, based on the player clicked on it, and the current turn
    # return True if a new piece has been selected, a move if it had been made, and False otherwise
        if self.selected:
            # if something is already selected:
            # checks if the piece can move to the cube that have been clicked
            # if not, maybe it's another piece of the same player, that he wants to select instead
            save_row = self.selected.row
            save_col = self.selected.col
            check = self.move(row, col)
            if not check:
                self.selected = None
                self.select(row, col)
            else:
                # returns the starter row and col of a piece before it moves, and than after
                places = str(save_row) + str(save_col) + str(row) + str(col)
                return places
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            # a new piece has been selected instead of the old one
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        return False

    def move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False
        return True

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == WHITE:
            self.turn = RED
        else:
            self.turn = WHITE

    def draw_vaild_moves(self, moves):
        # draws a circle where the valid moved are
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def winner(self):
        # return the color of the winner, if not
        return self.board.winner()
