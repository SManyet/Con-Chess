#!/usr/bin/python
# game.py: functional runner for py-chess

import curses, board, window, time

def main(screen):
    win = window.Window(screen)
    b = board.Board()
    game = True
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
            check, checkmate = b.test_check()
            if check:
                b.undo()
                if checkmate:
                    # win.checkmate()
                    pass
                else:
                    win.bad_move()
        else:
            win.bad_move()
        
        win.display(b)

curses.wrapper(main)
