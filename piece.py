#!/usr/bin/python
# piece.py: an abstract piece object to be implemented for each piece type

class Piece:
    def __init__(self, pos, color, symbol):
        self.pos = pos
        self.color = color
        self.symbol = symbol

    def set_pos(self, fpoint):
        self.pos = fpoint

    def get_valid_moves(self):
        pass

    def get_pos(self):
        return self.pos

    def get_color(self):
        return self.color

    def get_symbol(self):
        return self.symbol

