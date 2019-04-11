#!/usr/bin/python
# board.py: class to hold abstraction of the chess board

import piece

class Board:
    def __init__(self):
        self.board_array = self.init_board_array()
        self.white_cap = []
        self.black_cap = []

    def init_board_array(self):
        temp = [[piece.Piece((0, 0), False, 'r'), piece.Piece((1, 0), False, 'n'), piece.Piece((2, 0), False, 'b'), piece.Piece((3, 0), False, 'k'), piece.Piece((4, 0), False, 'q'), piece.Piece((5, 0), False, 'b'), piece.Piece((6, 0), False, 'n'), piece.Piece((7, 0), False, 'r')],
                [piece.Piece((0, 1), False, 'p'), piece.Piece((1, 1), False, 'p'), piece.Piece((2, 1), False, 'p'), piece.Piece((3, 1), False, 'p'), piece.Piece((4, 1), False, 'p'), piece.Piece((5, 1), False, 'p'), piece.Piece((6, 1), False, 'p'), piece.Piece((7, 1), False, 'p')],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [piece.Piece((0, 6), True, 'P'), piece.Piece((1, 6), True, 'P'), piece.Piece((2, 6), True, 'P'), piece.Piece((3, 6), True, 'P'), piece.Piece((4, 6), True, 'P'), piece.Piece((5, 6), True, 'P'), piece.Piece((6, 6), True, 'P'), piece.Piece((7, 6), True, 'P')],
        [piece.Piece((0, 7), 1, 'R'), piece.Piece((1, 7), True, 'N'), piece.Piece((2, 7), True, 'B'), piece.Piece((3, 7), True, 'K'), piece.Piece((4, 7), True, 'Q'), piece.Piece((5, 7), True, 'B'), piece.Piece((6, 7), True, 'N'), piece.Piece((7, 7), True, 'R')]]

        return temp

    def parse_input(self, move_str):
        ipoint, fpoint = eval(move_str)
        # Determine cap
        ipiece = self.board_array[ipoint[0]][ipoint[1]]
        fpiece = self.board_array[fpoint[0]][fpoint[1]]
        if fpiece:
            if (fpiece.get_color() == ipiece.get_color()):
                return False
            else:
                self.cap_piece(fpoint)
        self.move_piece(ipoint, fpoint)
        return True
    
    def move_piece(self, ipoint, fpoint):
        p = self.board_array[ipoint[0]][ipoint[1]]
        self.board_array[fpoint[0]][fpoint[1]] = p
        p.set_pos(fpoint)
        self.board_array[ipoint[0]][ipoint[1]] = None

    def cap_piece(self, fpoint):
        p = self.board_array[fpoint[0]][fpoint[1]]
        if p.get_color():
            self.black_cap.append(p)
        else:
            self.white_cap.append(p)

        self.board_array[fpoint[0]][fpoint[1]] = None
    
    def get_board_array(self):
        return self.board_array

    def get_white_cap(self):
        return self.white_cap

    def get_black_cap(self): 
        return self.black_cap

