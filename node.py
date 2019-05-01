#!/usr/bin/python
# class for implementing move and Node generation

from copy import deepcopy
from board import Board

class Node:
    def __init__(self, current_board=Board(), parent_move=None, node_weight=0, check=False):
        self.current_board = current_board
        self.parent_move = parent_move
        self.node_weight = node_weight
        self.child_nodes = {}
        self.check = check

    def gen_children(self):
        valid_moves = self.current_board.get_all_moves()
        for ipiece, move_list in valid_moves.items():
            if ipiece.get_color() == (self.current_board.turn % 2 == 1):
                ipoint = ipiece.get_pos()
                if ipiece.get_symbol() in ('k', 'K'):
                    queen_castle, king_castle = self.current_board.test_castle()
                    if queen_castle:
                        move_list.append("0-0-0")
                    if king_castle:
                        move_list.append("0-0")
                for fpoint in move_list:
                    child_board = deepcopy(self.current_board)
                    if fpoint == "0-0":
                        weight = 0
                        i, j = ipoint
                        child_board.move_piece(ipoint, (i, 6))
                        child_board.move_piece((i, 7), (i, 5))
                        child_move = fpoint
                    elif fpoint == "0-0-0":
                        weight = 0
                        i, j = ipoint
                        child_board.move_piece(ipoint, (i, 2))
                        child_board.move_piece((i, 0), (i, 3))
                        child_move = fpoint
                    else:
                        child_move = [ipoint, fpoint]
                        weight = child_board.move_piece(ipoint, fpoint)
                    if weight and not child_board.test_check(1):
                        if child_board.test_check(0): 
                            self.child_nodes[str(child_move)] = Node(current_board=child_board,
                                                                     parent_move=child_move,
                                                                     node_weight=weight+10,
                                                                     check=True)
                        else:
                            self.child_nodes[str(child_move)] = Node(current_board=child_board,
                                                                     parent_move=child_move,
                                                                     node_weight=weight)

                        
    def get_child(self, move):
            try:
                child = self.child_nodes[str(move)]
            except:
                return False
            return child
