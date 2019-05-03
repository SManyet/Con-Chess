#!/usr/bin/python
# board.py: class to hold abstraction of the chess board

import piece
import time

class Board:
    def __init__(self, board_array=None, turn=1, white_cap=[], black_cap=[], move_history=[], white_king=None, black_king=None):
        if board_array:
            self.board_array = board_array
        else:
            self.board_array = self.init_board_array()
        self.white_cap = white_cap
        self.black_cap = black_cap
        self.move_dict = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "-": False, "x": True}
        self.turn = turn
        self.white_moves = {}
        self.black_moves = {}
        if white_king and black_king:
            self.white_king, self.black_king = white_king, black_king
        else:
            self.white_king = self.board_array[7][4]
            self.black_king = self.board_array[0][4]


    def init_board_array(self):
        temp = [[piece.Rook((0, 0), False, 'r'), piece.Knight((0, 1), False, 'n'), piece.Bishop((0, 2), False, 'b'), piece.Queen((0, 3), False, 'q'), piece.King((0, 4), False, 'k'), piece.Bishop((0, 5), False, 'b'), piece.Knight((0, 6), False, 'n'), piece.Rook((0, 7), False, 'r')],
                [piece.Pawn((1, 0), False, 'p'), piece.Pawn((1, 1), False, 'p'), piece.Pawn((1, 2), False, 'p'), piece.Pawn((1, 3), False, 'p'), piece.Pawn((1, 4), False, 'p'), piece.Pawn((1, 5), False, 'p'), piece.Pawn((1, 6), False, 'p'), piece.Pawn((1, 7), False, 'p')],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [piece.Pawn((6, 0), True, 'P'), piece.Pawn((6, 1), True, 'P'), piece.Pawn((6, 2), True, 'P'), piece.Pawn((6, 3), True, 'P'), piece.Pawn((6, 4), True, 'P'), piece.Pawn((6, 5), True, 'P'), piece.Pawn((6, 6), True, 'P'), piece.Pawn((6, 7), True, 'P')],
        [piece.Rook((7, 0), 1, 'R'), piece.Knight((7, 1), True, 'N'), piece.Bishop((7, 2), True, 'B'), piece.Queen((7, 3), True, 'Q'), piece.King((7, 4), True, 'K'), piece.Bishop((7, 5), True, 'B'), piece.Knight((7, 6), True, 'N'), piece.Rook((7, 7), True, 'R')]]

        return temp

    
    def move_piece(self, ipoint, fpoint):
        if ipoint and fpoint:
            ipiece = self.board_array[ipoint[0]][ipoint[1]]
            fpiece = self.board_array[fpoint[0]][fpoint[1]]
            if fpiece:
                if fpiece.get_symbol() in ('k', 'K'):
                    return False
                else:
                    self.cap_piece(fpiece)
            self.board_array[fpoint[0]][fpoint[1]] = ipiece
            ipiece.set_pos(fpoint)
            ipiece.inc_move_count()
            self.board_array[ipoint[0]][ipoint[1]] = None
     
            symbol = ipiece.get_symbol()
            if symbol in ('k', 'K'):
                if symbol.isupper():
                    self.white_king = ipiece
                else:
                    self.black_king = ipiece

            self.inc_turn()
            return True
        else:
            return False


    def cap_piece(self, fpiece):
        if fpiece.get_color():
            self.black_cap.append(fpiece)
        else:
            self.white_cap.append(fpiece)
    

    def get_all_moves(self):
        all_moves = {}
        for row in self.board_array:
            for piece in row:
                if piece:
                    all_moves[piece] = piece.get_valid_moves(self.board_array)
        return all_moves
        

    def test_check(self, offset):
        self.get_all_moves()
        self.check = False
        if (self.turn - offset) % 2 == 1:
            king = self.white_king
            enemy_moves = self.black_moves
        else:
            king = self.black_king
            enemy_moves = self.white_moves
        if king:
            king_pos = king.get_pos()
            for move_list in enemy_moves.values():
                if king_pos in move_list:
                    self.check = True 
        return self.check



    def test_draw(self):
        for row in self.board_array:
            for piece in row:
                if piece and piece.get_symbol() not in ('k', 'K', 'b', 'B'):
                    return False
        return True
                        

    def test_castle(self):
        return self.castle_queen(), self.castle_king()

    def castle_king(self):
        king = None
        rook = None
        enemy_moves = None
        if self.turn % 2 == 1:
            king = self.white_king
            row = 7
            enemy_moves = self.black_moves
        else:
            king = self.black_king
            row = 0
            enemy_moves = self.white_moves
        rook = self.board_array[row][7]

        if rook and rook.get_move_count() == 0 and king.get_move_count() == 0:
            for col in (4, 5, 6):
                piece = self.board_array[row][col]
                if piece not in (king, None):
                    return False
                for move_list in enemy_moves.values():
                    if (row, col) in move_list:
                        return False
            return True
        else:
            return False


    def castle_queen(self):
        king = None
        rook = None
        row = 0
        enemy_moves = None
        if self.turn % 2 == 1:
            king = self.white_king
            row = 7
            enemy_moves = self.black_moves
        else:
            king = self.black_king
            enemy_moves = self.white_moves
        rook = self.board_array[row][0]

        if rook and rook.get_move_count() == 0 and king.get_move_count() == 0:
            for col in (1, 2, 3, 4):
                piece = self.board_array[row][col]
                if piece not in (king, None):
                    return False
                for move_list in enemy_moves.values():
                    if (row, col) in move_list:
                        return False
            return True
        else:
            return False





    
    def get_board_array(self):
        return self.board_array

    def get_white_cap(self):
        return self.white_cap

    def get_black_cap(self): 
        return self.black_cap

    def inc_turn(self):
        self.turn += 1

    def get_turn(self):
        return self.turn

