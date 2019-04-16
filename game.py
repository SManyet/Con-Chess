#!/usr/bin/python
# game.py: functional runner for py-chess

import curses, os, board, window

def main(screen):
    win = window.Window(screen)
    b = board.Board()
    game = True

    win.display(b)
    while game:

        move_str = win.input_move().decode("utf-8")
        if move_str == "exit":
            game = win.exit()
        elif b.parse_input(move_str):
            b.inc_turn()
        else:
            win.bad_move()
        
        win.display(b)

curses.wrapper(main)
