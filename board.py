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
        self.board_state = []

    def init_board_array(self):
        temp = [[piece.Rook((0, 0), False, 'r'), piece.Knight((0, 1), False, 'n'), piece.Bishop((0, 2), False, 'b'), piece.King((0, 3), False, 'k'), piece.Queen((0, 4), False, 'q'), piece.Bishop((0, 5), False, 'b'), piece.Knight((0, 6), False, 'n'), piece.Rook((0, 7), False, 'r')],
                [piece.Pawn((1, 0), False, 'p'), piece.Pawn((1, 1), False, 'p'), piece.Pawn((1, 2), False, 'p'), piece.Pawn((1, 3), False, 'p'), piece.Pawn((1, 4), False, 'p'), piece.Pawn((1, 5), False, 'p'), piece.Pawn((1, 6), False, 'p'), piece.Pawn((1, 7), False, 'p')],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [piece.Pawn((6, 0), True, 'P'), piece.Pawn((6, 1), True, 'P'), piece.Pawn((6, 2), True, 'P'), piece.Pawn((6, 3), True, 'P'), piece.Pawn((6, 4), True, 'P'), piece.Pawn((6, 5), True, 'P'), piece.Pawn((6, 6), True, 'P'), piece.Pawn((6, 7), True, 'P')],
        [piece.Rook((7, 0), 1, 'R'), piece.Knight((7, 1), True, 'N'), piece.Bishop((7, 2), True, 'B'), piece.King((7, 3), True, 'K'), piece.Queen((7, 4), True, 'Q'), piece.Bishop((7, 5), True, 'B'), piece.Knight((7, 6), True, 'N'), piece.Rook((7, 7), True, 'R')]]

        return temp

    def parse_input(self, move_str):
        move_str = move_str.lower()
        istr, cap, fstr = False, False, False

        if len(move_str) == 5:
            istr = self.eval_pos(move_str[:2])
            # cap = move_str[2]
            fstr = self.eval_pos(move_str[3:])
            if not istr or not fstr:
                return False
            else:
                ipoint = self.trans_rank_file(istr)
                fpoint = self.trans_rank_file(fstr)

            if self.move_piece(ipoint, fpoint):
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
    
    def move_piece(self, ipoint, fpoint):
        ipiece = self.board_array[ipoint[0]][ipoint[1]]
        if ipiece:
            valid_moves = ipiece.get_valid_moves(self.board_array)
            if ipiece.get_color() == (self.turn % 2 == 1) and fpoint in valid_moves:
                fpiece = self.board_array[fpoint[0]][fpoint[1]]
                if fpiece:
                    self.cap_piece(fpiece)
                self.board_array[fpoint[0]][fpoint[1]] = ipiece
                ipiece.set_pos(fpoint)
                self.board_array[ipoint[0]][ipoint[1]] = None
                return True
            else:
                return False
        else:
            return False


    def get_board_state(self):
        self.board_state = []
        for row in self.board_array:
            for piece in self.board_array[i]:
                if piece:
                    if ipiece.get_color() == (self.turn % 2 == 1):
                        valid_moves = piece.get_valid_moves()
                        [self.board_state.append(point) for point in valid_moves]
        return self.board_state




    def cap_piece(self, fpiece):
        if fpiece.get_color():
            self.black_cap.append(fpiece)
        else:
            self.white_cap.append(fpiece)
    
    
    
    
    
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

