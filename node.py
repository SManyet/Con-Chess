#!/usr/bin/python
# class for implementing move and Node generation

from copy import deepcopy
import board

class Node:
    def __init__(self, current_board, parent_move=None, weight=None):
        self.current_board = current_board
        self.parent_move = parent_move
        self.weight = weight
        self.child_nodes = self.gen_children()

    

    def gen_children(self):
        child_nodes = []
        if self.current_board.turn % 2 == 0:
            child_moves = self.current_board.white_moves
        else:
            child_moves = self.current_board.black_moves

        current_board = deepcopy(self.current_board)
        for piece, move_list in child_moves.items():
            ipoint = piece.get_pos()
            for fpoint in move_list:
                fpiece = current_board.board_array[fpoint[0]][fpoint[1]]
                cap = False
                if fpiece:
                    cap = True
                if current_board.move_piece(ipoint, fpoint, cap):
                    current_board.inc_turn()
                    if not current_board.test_check():
                        child_board = board.Board(board_array=current_board.board_array,
                                            turn=current_board.turn,
                                            white_king=current_board.white_king,
                                            black_king=current_board.black_king)
                        child_nodes.append(Node(child_board, parent_move=[ipoint, fpoint], weight=0))
                else:
                    continue
                current_board = deepcopy(self.current_board)
        return child_nodes

    def test_mate(self):
        return len(self.child_nodes) == 0
