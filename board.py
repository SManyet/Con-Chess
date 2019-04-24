#!/usr/bin/python
# board.py: class to hold abstraction of the chess board

import piece

class Board:
    def __init__(self):
        self.board_array = self.init_board_array()
        self.white_cap = []
        self.black_cap = []
        self.move_history = []
        self.move_dict = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "-": False, "x": True}
        self.turn = 1
        self.white_moves = {}
        self.black_moves = {}
        self.white_king = self.board_array[7][4]
        self.black_king = self.board_array[0][4]
        self.check = False
        self.checkmate = False

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


    def parse_input(self, move_str):
        istr, cap, fstr = False, False, False

        if move_str == "0-0":
            return self.castle_king()
        elif move_str == "0-0-0":
            return self.castle_queen()
        elif len(move_str) <= 5:
            istr = self.eval_pos(move_str[:2])
            cap = (move_str[2] in ('x', 'X'))
            fstr = self.eval_pos(move_str[3:])
            if not istr or not fstr:
                return False
            else:
                ipoint = self.trans_rank_file(istr)
                fpoint = self.trans_rank_file(fstr)

            if self.move_piece(ipoint, fpoint, cap):
                self.move_history.append(move_str)
                return True
            else:
                return False


    def eval_pos(self, pos):
        if ord(pos[0]) > 104 or ord(pos[0]) < 97:
            return False
        elif ord(pos[1]) > 56 or ord(pos[1]) < 49:
            return False
        else:
            return pos


    def trans_rank_file(self, rank_file):
        findex = 8 - int(rank_file[1])
        rindex = self.move_dict[rank_file[0]]
        return (findex, rindex)
    
    def move_piece(self, ipoint, fpoint, cap):
        ipiece = self.board_array[ipoint[0]][ipoint[1]]
        if ipiece: 
            valid_moves = []
            if ipiece.get_color():
                valid_moves = self.white_moves[ipiece]
            else:
                valid_moves = self.black_moves[ipiece]

            if ipiece.get_color() == (self.turn % 2 == 1) and fpoint in valid_moves:
                fpiece = self.board_array[fpoint[0]][fpoint[1]]
                if fpiece:
                    if not cap or fpiece.get_symbol() in ('k', 'K'):
                        return False
                    else:
                        self.cap_piece(fpiece)
                self.board_array[fpoint[0]][fpoint[1]] = ipiece
                ipiece.set_pos(fpoint)
                ipiece.inc_move_count()
                self.board_array[ipoint[0]][ipoint[1]] = None
                
                symbol = ipiece.get_symbol()
                if symbol in ('p', 'P') and fpoint[0] in (0, 8):
                    if symbol.isupper():
                        self.board_array[fpoint[0]][fpoint[1]] = piece.Queen(fpoint, ipiece.get_color(), 'Q')
                    elif symbol.islower():
                        self.board_array[fpoint[0]][fpoint[1]] = piece.Queen(fpoint, ipiece.get_color(), 'q')
                    else:
                        return False

                return True
            else:
                return False
        else:
            return False


    def cap_piece(self, fpiece):
        if fpiece.get_color():
            self.black_cap.append(fpiece)
        else:
            self.white_cap.append(fpiece)
    

    def get_all_moves(self):
        self.white_moves.clear()
        self.black_moves.clear()

        for row in self.board_array:
            for piece in row:
                if piece:
                    if piece.get_color():
                        self.white_moves[piece] = piece.get_valid_moves(self.board_array)
                    else:
                        self.black_moves[piece] = piece.get_valid_moves(self.board_array)
        

    def test_check(self):
        self.get_all_moves()
        self.check = False
        self.checkmate = False
        if (self.turn - 1) % 2 == 1:
            king = self.white_king
            enemy_moves = self.black_moves
        else:
            king = self.black_king
            enemy_moves = self.white_moves
        if king:
            # king_moves = king.get_valid_moves(self.board_array)
            king_pos = king.get_pos()
            for move_list in enemy_moves.values():
                if king_pos in move_list:
                    self.check = True
                # king_moves = [move for move in king_moves if move not in move_list]
                # if self.check and len(king_moves) == 0:
                #     self.checkmate = True
        
        return self.check, self.checkmate


    def undo(self):
        self.turn -= 1
        move_str = self.move_history.pop()
        ipoint = self.trans_rank_file(move_str[:2])
        fpoint = self.trans_rank_file(move_str[3:])
        cap = (move_str[2] in ('x', 'X'))

        ipiece = self.board_array[fpoint[0]][fpoint[1]]
        self.board_array[ipoint[0]][ipoint[1]] = ipiece
        ipiece.set_pos(ipoint)
        fpiece = None
        if cap:
            if ipiece.get_color():
                fpiece = self.white_cap.pop()
            else:
                fpiece = self.black_cap.pop()
                
        self.board_array[fpoint[0]][fpoint[1]] = fpiece
        if fpiece:
            fpiece.set_pos(fpoint)



    def castle_king(self):
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
        rook = self.board_array[row][7]

        if rook and rook.get_move_count() == 0 and king.get_move_count() == 0:
            for col in (4, 5, 6):
                piece = self.board_array[row][col]
                if piece not in (king, None):
                    return False
                for move_list in enemy_moves.values():
                    if (row, col) in move_list:
                        return False
            self.board_array[row][5] = rook
            rook.set_pos((row, 5))
            rook.inc_move_count()
            self.board_array[row][6] = king
            king.set_pos((row, 6))
            king.inc_move_count()
            self.board_array[row][4] = None
            self.board_array[row][7] = None
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
            self.board_array[row][3] = rook
            rook.set_pos((row, 3))
            rook.inc_move_count()
            self.board_array[row][2] = king
            king.set_pos((row, 2))
            king.inc_move_count()
            self.board_array[row][4] = None
            self.board_array[row][0] = None
            return True
        else:
            return False






    def get_checkmate(self):
        return self.checkmate
    
    def get_board_array(self):
        return self.board_array

    def get_white_cap(self):
        return self.white_cap

    def get_black_cap(self): 
        return self.black_cap

    def get_move_history(self):
        return self.move_history

    def inc_turn(self):
        self.turn += 1

    def get_turn(self):
        return self.turn

