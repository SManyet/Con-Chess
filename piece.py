#!/usr/bin/python
# piece.py: an abstract piece object to be implemented for each piece type

class Piece:
    def __init__(self, pos, color, symbol):
        self.pos = pos
        self.color = color
        self.symbol = symbol
        self.valid_moves = []
        self.move_count = 0

    def follow_path(self, board_array, inc):
        i, j = self.pos
        di, dj = inc
        count = 1
        while True:
            row = i+count*di
            col = j+count*dj
            if -1 < row < 8 and -1 < col < 8:
                piece = board_array[row][col]
                if piece:
                    if piece.get_color() != self.color:
                        self.valid_moves.append((row, col))
                        return False
                    else:
                        return False
                else: 
                    self.valid_moves.append((row, col))
                    count+=1
            else:
                return False
    
    def follow_template(self, board_array, template):
        i, j = self.pos
        for point in template:
            row = i + point[0]
            col = j + point[1]
            if -1 < row < 8 and -1 < col < 8:
                piece = board_array[row][col]
                if piece:
                    if piece.get_color() != self.color:
                        self.valid_moves.append((row, col))
                else:
                    self.valid_moves.append((row, col))


    def inc_move_count(self):
        self.move_count += 1

    def get_move_count(self):
        return self.move_count

    def set_pos(self, fpoint):
        self.pos = fpoint

    def get_pos(self):
        return self.pos

    def get_color(self):
        return self.color

    def get_symbol(self):
        return self.symbol
    
    def get_value(self):
        return self.value

class King(Piece):
    def __init__(self, pos, color, symbol):
        super().__init__(pos, color, symbol)
        self.template = [(1, 1), (1, 0), (1, -1), (-1, -1),
                         (-1, 0), (-1, 1), (0, 1), (0, -1)]
        self.value = 0


    def get_valid_moves(self, board_array):
        self.valid_moves.clear()
        self.follow_template(board_array, self.template)
        return self.valid_moves

class Queen(Piece):
    def __init__(self, pos, color, symbol):
        super().__init__(pos, color, symbol)
        if self.color:
            self.value = 9
        else:
            self.value = -9

    def get_valid_moves(self, board_array):
        self.valid_moves.clear()
        self.follow_path(board_array, (1,0))
        self.follow_path(board_array, (-1,0))
        self.follow_path(board_array, (0,1))
        self.follow_path(board_array, (0,-1))
        self.follow_path(board_array, (1,1))
        self.follow_path(board_array, (-1,1))
        self.follow_path(board_array, (1,-1))
        self.follow_path(board_array, (-1,-1))
        return self.valid_moves


class Bishop(Piece):
    def __init__(self, pos, color, symbol):
        super().__init__(pos, color, symbol)
        if self.color:
            self.value = 3
        else:
            self.value = -3

    def get_valid_moves(self, board_array): 
        self.valid_moves.clear()
        self.follow_path(board_array, (1,1))
        self.follow_path(board_array, (-1,1))
        self.follow_path(board_array, (1,-1))
        self.follow_path(board_array, (-1,-1))
        return self.valid_moves


class Knight(Piece):
    def __init__(self, pos, color, symbol):
        super().__init__(pos, color, symbol)
        self.template = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                         (1, 2), (-1, 2), (1, -2), (-1, -2)]
        if self.color:
            self.value = 3
        else:
            self.value = -3

    def get_valid_moves(self, board_array):
        self.valid_moves.clear()
        self.follow_template(board_array, self.template)
        return self.valid_moves


class Rook(Piece):
    def __init__(self, pos, color, symbol):
        super().__init__(pos, color, symbol)
        if self.color:
            self.value = 5
        else:
            self.value = -5

    def get_valid_moves(self, board_array):
        self.valid_moves.clear()
        self.follow_path(board_array, (1, 0))
        self.follow_path(board_array, (-1, 0))
        self.follow_path(board_array, (0, 1))
        self.follow_path(board_array, (0, -1))
        return self.valid_moves

class Pawn(Piece):
    def __init__(self, pos, color, symbol):
        super().__init__(pos, color, symbol)
        if self.color:
            self.value = 1
        else:
            self.value = -1

    def get_valid_moves(self, board_array):
        self.valid_moves.clear()
        i, j = self.pos
        offset = None
        if self.color:
            offset = -1
        else:
            offset = 1

        for col in [j-1, j, j+1]:
            if -1 < col < 8:
                piece = board_array[i+offset][col]
                if piece:
                    if col != j:
                        if piece.get_color() != self.color:
                            self.valid_moves.append((i+offset, col))
                elif col == j:
                    self.valid_moves.append((i+offset, col))
                    if self.move_count == 0 and not board_array[i+2*offset][j]:
                        self.valid_moves.append((i+2*offset, j))
        return self.valid_moves

