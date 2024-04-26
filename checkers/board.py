import pygame
from checkers.piece import Piece
from .constants import RED, BLACK, WHITE, ROWS, SQUARE_SIZE, COLS


class Board:
    def __init__(self):
    # creates the board. variables:
    # board - an 8x8 list representing the current state of the board,
    # each place contains a piece or a blank cube(that is marked with 0)
    # red_left, white_left - how much pieces of each color are left
    # white_kings, red_kings - how much kings are on each side
        self.board = []
        self.red_left = self.white_left = 12
        self.white_kings = self.red_kings = 0
        self.create_board()

    def draw_cubes(self, window):
    # Draw the board itself
        window.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                 pygame.draw.rect(window, WHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
    # creates the list of the board, putting 0 where is empty
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if ((row + 1) % 2) == col % 2:
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def get_piece(self, row, col):
    # return the piece in a certain position
        return self.board[row][col]

    def move(self, piece, row, col):
        # moves a piece, turns it into king if needed, and updates the board list
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        if (row == 0 or row == ROWS - 1) and (piece.isking is not True):
        # Checks if the piece arrived at one the most upper or downer row
        # which means it should become a king
            piece.turn_into_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def draw_board(self, window):
    # draws all the board, including the pieces and the cubes
        self.draw_cubes(window)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw_piece(window)

    def remove(self, pieces):
        # removes the pieces that has been eaten in a turn, and update the variables
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == WHITE:
                    self.white_left -= 1
                else:
                    self.red_left -= 1

    def get_valid_moves(self, piece):
        # gets a piece, and returns according to the place and color of the piece
        # a list containing the possible moves it can do
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row
        if piece.color == RED or piece.isking:
            # if the color is red or the piece is a king - it means that it can move up
            moves.update(self.go_left(left, piece.color, -1, max(row - 3, -1), row - 1))
            moves.update(self.go_right(right, piece.color, -1, max(row - 3, -1), row - 1))
        if piece.color == WHITE or piece.isking:
            # if the color is white or the piece is a king - it means that it can move down
            moves.update(self.go_left(left, piece.color, 1, min(row + 3, ROWS), row + 1))
            moves.update(self.go_right(right, piece.color, 1, min(row + 3, ROWS), row + 1))
        return moves

    def go_left(self, left, color, step, stop, start, skipped=[]):
        # checks about possible moves in the left side of the piece
        # moves is a dictionary which stores possible moves, where the key is from where it comes,
        # and the value is where it can go. skipped stores the piece that have been jumped to.
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = skipped + last
                else:
                    moves[(r, left)] = last
                if last:
                    # check if double or triple jump ect, is possible
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self.go_left(left - 1, color, step, row, r+step, skipped=last))
                    moves.update(self.go_right(left + 1, color, step, row, r+step, skipped=last))
                break
            elif current.color == color:
                # same color as the piece, so it can not move over it
                break
            else:
                # the other piece is the opposing color, maybe we can move our piece to eat it
                last = [current]
            left -= 1
        return moves

    def go_right(self, right, color, step, stop, start, skipped=[]):
        # checks about possible moves in the right side of the piece
        # moves is a dictionary which stores possible moves, where the key is from where it comes,
        # and the value is where it can go. skipped stores the piece that have been jumped to.
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = skipped + last
                else:
                    moves[(r, right)] = last
                if last:
                    # check if double or triple jump ect, is possible
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self.go_left(right - 1, color, step, row, r+step, skipped=last))
                    moves.update(self.go_right(right + 1, color, step, row, r+step, skipped=last))
                break
            elif current.color == color:
                # same color as the piece, so it can not move over it
                break
            else:
                # the other piece is the opposing color, maybe we can move our piece to eat it
                last = [current]
            right += 1
        return moves

    def winner(self):
        # checks if there is a winner, if so return it's color
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        return None




