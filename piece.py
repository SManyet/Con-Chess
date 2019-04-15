#!/usr/bin/python
# piece.py: an abstract piece object to be implemented for each piece type

class Piece:
    def __init__(self, pos, color, symbol):
        self.pos = pos
        self.color = color
        self.symbol = symbol
        self.valid_moves = []

    def set_pos(self, fpoint):
        self.pos = fpoint

    def get_pos(self):
        return self.pos

    def get_color(self):
        return self.color

    def get_symbol(self):
        return self.symbol

class King(Piece):
    def __init__(self, pos, color, symbol):
        super().__init__(pos, color, symbol)

    def get_valid_moves(self, board_array):
        '''
        TODO: castle and castle through check
        '''
    
        i, j = self.pos

        for row in (i-1, i, i+1):
            if i+1 != 8 and i-1 != -1:
                for col in (j-1, j, j+1):
                    if col+1 != 8 and col-1 != -1:
                        p = board_array[i][j]
                        if p:
                            if p.get_color() != self.color:
                                self.valid_moves.append((i, j))
                        else:
                            self.valid_moves.append((i, j))
        
        return self.valid_moves

class King(Piece):
    def __init__(self, pos, color, symbol):
        super().__init__(pos, color, symbol)

    def get_valid_moves(self, board_array):
        '''
        TODO: castle and castle through check
        '''
    
        i, j = self.pos

        for row in [i-1, i, i+1]:
            if row != 8 and row != -1:
                for col in [j-1, j, j+1]:
                    if col != 8 and col != -1:
                        p = board_array[row][col]
                        if p:
                            if p.get_color() != self.color:
                                self.valid_moves.append((row, col))
                        else:
                            self.valid_moves.append((row, col))
        
        return self.valid_moves

class Queen(Piece):
    def __init__(self, pos, color, symbol):
        super().__init__(pos, color, symbol)

    def get_valid_moves(self, board_array):
        for i in range(8):
            for j in range(8):
                self.valid_moves.append((i, j))
        return self.valid_moves

class Bishop(Piece):
    def __init__(self, pos, color, symbol):
        super().__init__(pos, color, symbol)

    def get_valid_moves(self, board_array):
        for i in range(8):
            for j in range(8):
                self.valid_moves.append((i, j))
        return self.valid_moves

class Knight(Piece):
    def __init__(self, pos, color, symbol):
        super().__init__(pos, color, symbol)

    def get_valid_moves(self, board_array):
        for i in range(8):
            for j in range(8):
                self.valid_moves.append((i, j))
        return self.valid_moves

class Rook(Piece):
    def __init__(self, pos, color, symbol):
        super().__init__(pos, color, symbol)

    def get_valid_moves(self, board_array):
        for i in range(8):
            for j in range(8):
                self.valid_moves.append((i, j))
        return self.valid_moves

class Pawn(Piece):
    def __init__(self, pos, color, symbol):
        super().__init__(pos, color, symbol)

    def get_valid_moves(self, board_array):
        i, j = self.pos
        offset = None
        if self.color:
            offset = -1
        else:
            offset = 1

        for col in (j-1, j, j+1):
            if col != -1 and col != 8:
                piece = board_array[i+offset][col]
                if piece and col != j:
                    if piece.get_color() != self.color:
                        self.valid_moves.append((i+offset, col))
                else:
                    self.valid_moves.append((i+offset, col))
        return self.valid_moves




        for i in range(8):
            for j in range(8):
                self.valid_moves.append((i, j))
        return self.valid_moves
