#!/usr/bin/python
# class file for an AI that simply makes random moves from all available moves
from random import choice

class Random:

    def make_move(self, nodes):
        return choice(list(nodes.values()))

class Human:
    pass

class Minimax:
    pass



