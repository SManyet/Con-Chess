# reference file for python-curses

import curses as c
import random

def main(stdscr):
    # Clear screen
    stdscr.clear()
    c.cbreak()
    c.noecho()
    
    xi, yi = 0, 0
    index = 0
    maxlines, maxcols = c.LINES - 1, c.COLS - 1

    y = [0, maxlines, 0]
    x = [0, maxcols // 2, maxcols]

    stdscr.addch(y[0], x[0], '0')
    stdscr.addch(y[1], x[1], '1')
    stdscr.addch(y[2], x[2], '2')

    yi = random.randint(0, 100000) % maxlines
    xi = random.randint(0, 100000) % maxcols
    stdscr.addch(yi, xi, '.')

    for i in range(10000):
        index = random.randint(0, 100000) % 3

        yi = (yi + y[index]) // 2
        xi = (xi + x[index]) // 2

        stdscr.addch(yi, xi, '*')
        stdscr.refresh()

    stdscr.addstr(maxlines, 0, "Press any key to quit")
    stdscr.refresh()
    stdscr.getch()
    c.endwin()
    

c.wrapper(main)
