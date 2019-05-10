#!/usr/bin/python
# game.py: functional runner for py-chess

import curses
from window import Window
from node import ConcurrentNode, SerialNode, HybridNode
from AI import Random, Human, Minimax
from time import sleep

def main(screen):
    window = Window(screen)
    player1, player2, node_type = window.settings()
    settings_dict = {"human": Human(),
                     "random": Random(),
                     "minimax": Minimax(),
                     "serial": SerialNode(),
                     "concurrent": ConcurrentNode(),
                     "hybrid": SerialNode()}
    player1 = settings_dict[player1]
    player2 = settings_dict[player2]
    node = settings_dict[node_type]
    window.display(node.current_board)

    while True:
        if node.current_board.test_draw():
            window.draw()
            break
        node.gen_children()
        if len(node.child_nodes) == 0:
            window.checkmate()
            break
        if node.current_board.turn % 2 == 1:
            temp_node = player1.make_move(node, window)
            if temp_node == "exit":
                window.exit()
                break
            elif not temp_node:
                window.bad_move()
                continue           
            else:
                node = temp_node
        else:
            temp_node = player2.make_move(node, window)     
            if temp_node == "exit":
                window.exit()
                break
            elif not temp_node:
                window.bad_move()
                continue
            else:
                node = temp_node
        if node:
            if node.check:
                window.check()
            else:
                window.good_move()
        else:
            window.bad_move()
        
        window.display(node.current_board)

curses.wrapper(main)
