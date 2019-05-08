#!usr/bin/python
# window.py: class file for managing display with curses

import curses

class Window:
    def __init__(self, screen):
        self.screen = screen
        self.maxlines = curses.LINES - 1
        self.maxcols = curses.COLS - 1
        self.move_dict = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

        screen.clear()
        curses.cbreak()
        curses.echo()
    


    '''
    Methods for displaying the game to terminal should remain indepent
    from other processes to assist training speed
    '''
    def settings(self):
        return self.player(1), self.player(2), self.node_type()

    def player(self, i):
        self.screen.addstr(self.maxlines - 1, 1, "Player {}: human, random, minimax [depth]".format(i))
        player_str = self.screen.getstr(self.maxlines, 1).decode("utf-8").lower()
        self.screen.refresh()
        self.screen.clear()
        if "human" in player_str:
            return "human"
        elif "random" in player_str:
            return "random"
        elif "minimax" in player_str:
            return "minimax"
        else:
            return False

    def node_type(self):
        self.screen.addstr(self.maxlines - 1, 1, "Node Type: serial, concurrent, or hybrid"
                )
        node_type = self.screen.getstr(self.maxlines, 1).decode("utf-8").lower()
        self.screen.refresh()
        self.screen.clear()
        if "serial" in node_type:
            return "serial"
        elif "concurrent" in node_type:
            return "concurrent"
        elif "hybrid" in node_type:
            return "hybrid"
        else:
            return False






    def display(self, board):
        board_array = board.get_board_array()
        
        self.board_display(board_array)
        self.cap_display(board.get_white_cap(), board.get_black_cap())
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

    def turn_display(self, turn):
        self.screen.addstr(0, 36, str(turn))

    
    def parse_input(self, move_str):
        if move_str == "exit":
            return "exit"
        if move_str == "0-0-0":
            return move_str 
        elif move_str == "0-0":
            return move_str
        elif len(move_str) == 5:
            istr = self.eval_pos(move_str[:2])
            fstr = self.eval_pos(move_str[3:])
            if not istr or not fstr:
                return False
            else:
                ipoint = self.trans_rank_file(istr)
                fpoint = self.trans_rank_file(fstr)
            if ipoint and fpoint:
                return [ipoint, fpoint]
            else:
                return False
        else:
            return False


    def eval_pos(self, pos):
        if ord(pos[0]) > 104 or ord(pos[0]) < 97:
            return False
        elif ord(pos[1]) > 56 or ord(pos[1]) < 49:
            return False
        else:
            return pos


    def trans_rank_file(self, rank_file):
        findex = 8 - int(rank_file[1])
        rindex = self.move_dict[rank_file[0]]
        return (findex, rindex)








    ''' get, set, and other functional methods'''

    def check(self):
        self.screen.addstr(15, self.maxcols//2, "Check        ")

    def draw(self):
        self.screen.addstr(15, self.maxcols//2, "Draw         ")
        self.exit()

    def checkmate(self):
        self.screen.addstr(15, self.maxcols//2, "Checkmate    ")
        self.exit()

    def bad_move(self):
        self.screen.addstr(15, self.maxcols//2, "invalid input")
    
    def good_move(self):
        self.screen.addstr(15, self.maxcols//2, "valid input  ")

    def input_move(self):
        move_str = self.screen.getstr(self.maxlines, 1).decode("utf-8").lower()
        return self.parse_input(move_str)
    
    def exit(self):
        self.screen.addstr(self.maxlines - 1, 1, "press ENTER to exit")
        self.screen.getch()
        self.screen.refresh()
        curses.endwin()
