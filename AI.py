#!/usr/bin/python
# class file for an AI that simply makes random moves from all available moves
from random import choice

class Random:
    def make_move(self, node, window):
        children = node.child_nodes
        return choice(list(children.values()))

class Human:
    def make_move(self, node, window):
        move = window.input_move()
        if move:
            if "exit" in move:
                return "exit"
            else:
                return node.get_child(move)
        else:
            return False

class Minimax:
    def make_move(self, node, window):
        future_node = self.search_future(node, 2)
        next_move = future_node.move_history[-2]
        if len(next_move) == 1:
            next_move = next_move[0]
        next_node = node.child_nodes[next_move]
        if next_node:
            return next_node

    def search_future(self, node, depth):
        if len(node.child_nodes) == 0:
            node.gen_children()
            if len(node.child_nodes) == 0:
                return node
        if depth == 0:
            return node
        elif node.current_board.turn % 2 == 1:
            max_weight = node.weight
            max_child = None
            for child in node.child_nodes.values():
                grandchild = self.search_future(child, depth - 1)
                if grandchild.weight >= max_weight:
                    max_weight = grandchild.weight
                    max_child = grandchild
            if max_child:
                return max_child
            else:
                x = 5 / 0
        else:
            min_weight = node.weight
            min_child = None
            for child in node.child_nodes.values():
                grandchild = self.search_future(child, depth - 1)
                if grandchild.weight <= min_weight:
                    min_weight = grandchild.weight
                    min_child = grandchild

            if min_child:
                return min_child
            else:
                x = 5 / 0





