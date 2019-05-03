#!/usr/bin/python
# class file for an AI that simply makes random moves from all available moves
from random import choice

class RandomAI:

    def make_move(self, nodes):
        return choice(list(nodes.values()))



