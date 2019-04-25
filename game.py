#!/usr/bin/python
# game.py: functional runner for py-chess

import curses, board, window

def main(screen):
    win = window.Window(screen)
    b = board.Board()
    win.display(b)
    b.get_all_moves()

    while True:

        move_str = win.input_move().decode("utf-8").lower()
        if move_str == "exit":
            win.exit()
            break
        elif b.parse_input(move_str):
            b.inc_turn()
            win.good_move()
            if b.test_check():
                if b.test_mate():
                    win.checkmate()
                    break
                else:
                    b.undo()
                    win.bad_move()

        else:
            win.bad_move()
        
        win.display(b)

curses.wrapper(main)
