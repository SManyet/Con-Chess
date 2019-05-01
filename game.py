#!/usr/bin/python
# game.py: functional runner for py-chess

import curses
from window import Window
from node import Node

def main(screen):
    window = Window(screen)
    node = Node()
    window.display(node.current_board)

    while True:
        node.gen_children()
        if len(node.child_nodes) == 0:
            window.checkmate()
            break
        move = window.input_move()
        if move == "exit":
            window.exit()
            break
        elif move:
            child = node.get_child(move)
            if child:
                node = child
                if child.check:
                    window.check()
                else:
                    window.good_move()
            else:
                window.bad_move()
        else:
            window.bad_move()
        
        window.display(node.current_board)

curses.wrapper(main)
