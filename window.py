#!usr/bin/python
# window.py: class file for managing display with curses

import curses
# import board
from curses.textpad import rectangle

class Window:
    def __init__(self, screen):
        self.screen = screen
        self.maxlines = curses.LINES - 1
        self.maxcols = curses.COLS - 1

        screen.clear()
        curses.cbreak()
        curses.echo()
    


    '''
    Methods for displaying the game to terminal should remain indepent
    from other processes to assist training speed
    '''
    def display(self, board):
        board_array = board.get_board_array()
        
        self.board_display(board_array)
        self.cap_display(board.get_white_cap(), board.get_black_cap())
        self.move_display(board.get_move_history())
        self.turn_display(board.get_turn())

        self.screen.addstr(self.maxlines, 1, "                      ")

        self.screen.refresh()

    def board_display(self, board_array):
        counter = 0
        for c in range(34):
            for l in range(17):
                if c % 4 == 1:
                    self.screen.addch(l, c, '|')
                elif l % 2 == 0 and c > 1:
                    self.screen.addch(l, c, '-')
                elif c % 4 == 3:
                    # translate between screen and board indicies
                    i = counter // 8
                    j = counter % 8

                    # draw rank and file
                    self.screen.addch(l, 0, str(8 - j))
                    self.screen.addch(17, c, chr(i + 65))
                    
                    # draw pieces
                    piece = board_array[j][i]
                    if piece:
                        self.screen.addch(l, c, piece.get_symbol())
                    else:
                        self.screen.addch(l, c, ' ')
                    counter += 1

    def cap_display(self, white_cap, black_cap):
        white_index = 0
        black_index = 0
        for c in range(40, 47):
            for l in range(13):
                # self.screen.addch(l, c, '#')
                if c == 40 or c == 43 or c == 46:
                    self.screen.addch(l, c, "|")
                elif l == 0 or l == 2 or l == 12:
                    self.screen.addch(l, c, '-')
                elif l > 2:
                    if white_index < len(white_cap):
                        symbol = white_cap[white_index].get_symbol()
                        self.screen.addch(l, c, symbol)
                        white_index += 1
                    elif black_index < len(black_cap) and c > 43:
                        symbol = black_cap[black_index].get_symbol()
                        self.screen.addch(l, c, symbol)
                        black_index += 1


        self.screen.addch(1, 41, 'W')
        self.screen.addch(1, 44, 'B')
    

    def move_display(self, move_history):
        index = 0
        for c in range(49, 65):
            for l in range(13):
                if c == 49 or c == 64:
                    self.screen.addch(l, c, '|')
                elif l == 0 or l == 12:
                    self.screen.addch(l, c, '-')
                elif l > 0 and l - 1 < len(move_history):
                    self.screen.addstr(l, 50, move_history[len(move_history) - l])

    def turn_display(self, turn):
        self.screen.addstr(0, 36, str(turn))

    


    ''' get, set, and other functional methods'''

    # def checkmate(self):
    #    pass

    def bad_move(self):
        self.screen.addstr(15, self.maxcols//2, "invalid input")
    
    def good_move(self):
        self.screen.addstr(15, self.maxcols//2, "invalid input")

    def input_move(self):
        return self.screen.getstr(self.maxlines, 1)
    
    def exit(self):
        self.screen.addstr(self.maxlines - 1, 1, "press ENTER to exit")
        self.screen.getch()
        curses.endwin()
        return False
