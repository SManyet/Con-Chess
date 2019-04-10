#!/usr/bin/python
# game.py: functional runner for py-chess

import curses, board, window

def main(screen):
    win = window.Window(screen)
    b = board.Board(win)
    
    win.display(b)
    
    movestr = screen.getch()
    cap, move b.parse_input(movestr)
    
    '''
    move [(ipoint), (fpoint)] if valid, empty otherwise
    '''
    
    if move:
        if cap:
            b.cap

    win.display(b)

    win.exit()

curses.wrapper(main)
