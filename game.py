#!/usr/bin/python
# game.py: functional runner for py-chess

import curses, board, window

def main(screen):
    win = window.Window(screen)
    b = board.Board()
    game = True

    win.display(b)
    while game:

        move_str = win.get_move()
        if move_str == b'exit':
            game = win.exit()
        elif not b.parse_input(move_str):
            win.bad_move()
    
        win.display(b)

curses.wrapper(main)
