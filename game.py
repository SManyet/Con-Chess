#!/usr/bin/python
# game.py: functional runner for py-chess

import curses
from window import Window
from node import Node
from randomAI import RandomAI
import time

def main(screen):
    window = Window(screen)
    node = Node()
    window.display(node.current_board)
    opponent = RandomAI()

    while True:
        if node.current_board.test_draw():
            window.draw()
            time.sleep(1)
            node = Node()
        node.gen_children()
        if len(node.child_nodes) == 0:
            window.checkmate()
            break
        if True:
            node = opponent.make_move(node.child_nodes)
            if not node:
                continue
            move = None
            # time.sleep(.1)
        else:
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
