#!/usr/bin/python
# class for implementing move and Node generation

from copy import deepcopy
from board import Board
from piece import Queen
from time import sleep
import multiprocessing

class Node:
    def __init__(self, current_board=Board(), parent_move=None, node_weight=0, check=False, draw=False):
        self.current_board = current_board
        self.parent_move = parent_move
        self.node_weight = node_weight
        self.child_nodes = {}
        self.check = check
        self.draw = draw


                    


    def eval_node(self, ipoint, fpoint, symbol, current_board, queue):
        child_board = deepcopy(current_board)
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
        elif fpoint[0] in (0, 7) and symbol in ('p', 'P'):
            child_board.board_array[ipoint[0]][ipoint[1]] = None
            if symbol.islower():
                child_board.board_array[fpoint[0]][fpoint[1]] = Queen((fpoint[0], fpoint[1]), False, 'q')
            else:
                child_board.board_array[fpoint[0]][fpoint[1]] = Queen((fpoint[0], fpoint[1]), True, 'Q')
            child_board.inc_turn()
            weight = 100
            child_move = [ipoint, fpoint]
        else:
            child_move = [ipoint, fpoint]
            weight = child_board.move_piece(ipoint, fpoint)
        if weight and not child_board.test_check(1):
            if child_board.test_check(0): 
                queue.put(Node(current_board=child_board, parent_move=child_move, node_weight=weight, check=True))
            else:
                queue.put(Node(current_board=child_board, parent_move=child_move, node_weight=weight))




    def gen_children(self):
        valid_moves = self.current_board.get_all_moves()
        processes = []
        queue = multiprocessing.Manager().Queue()
        for ipiece, move_list in valid_moves.items():
            if ipiece.get_color() == (self.current_board.turn % 2 == 1):
                ipoint = ipiece.get_pos()
                symbol = ipiece.get_symbol()
                if symbol in ('k', 'K'):
                    queen_castle, king_castle = self.current_board.test_castle()
                    if queen_castle:
                        move_list.append("0-0-0")
                    if king_castle:
                        move_list.append("0-0")
                for fpoint in move_list:
                    proc = multiprocessing.Process(target=self.eval_node, args=(ipoint, fpoint, symbol, self.current_board, queue,))
                    processes.append(proc)
                    proc.start()
                for p in processes:
                    p.join()
                while True:
                    try:
                        child_node = queue.get(False)
                        move = str(child_node.parent_move)
                        self.child_nodes[move] = child_node
                    except:
                        break


    def get_child(self, move):
            try:
                child = self.child_nodes[str(move)]
            except:
                return False
            return child
