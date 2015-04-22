from __future__ import absolute_import
import random, timeit
from engines import Engine
from copy import deepcopy

class StudentEngine(Engine):
    """ Game engine that implements a simple fitness function maximizing the
    difference in number of pieces in the given color's favor. """
    def __init__(self):
        self.alpha_beta = False
        self.count = 0
        self.a = 0
        self.b = 0
        self.start_time = 0
        self.move_num = 0
        self.change_strat = False
        self.num_nodes = 1
        self.nodes_generated = False
        self.log_boards = False
        self.boards_seen = {}
        self.branching = False
        self.num_elem = 1
        self.time = False
        self.end_time = 0
        self.total_avg = 0

    def get_move(self, board, color, move_num=None,
	             time_remaining=None, time_opponent=None):
        """ Return a move for the given color that maximizes the difference in 
        number of pieces for that color. """
        # initialize the start time of this move
        self.start_time = timeit.default_timer()

        self.move_num += 1

        moves = board.get_legal_moves(color)
        self.num_elem += 1
        self.num_nodes += len(moves)

        if self.nodes_generated:
            print 'Nodes generated: %s' % self.num_nodes

        if self.log_boards:
            print self.get_duplicates_count()

        if self.branching:
            print 'Branching factor: %s' % (self.num_nodes / float(self.num_elem))

        if (self.alpha_beta == False): 
            if time_remaining < 4:
                if self.time:
                    self.end_time = timeit.default_timer()
                    self.total_avg += (self.end_time - self.start_time)
                    print self.avg_time()
                return random.choice(moves)
            
            m = max(moves, key=lambda move: self.min_val(board, color, color, move, 3, time_remaining))
            if self.time:
                self.end_time = timeit.default_timer()
                self.total_avg += (self.end_time - self.start_time)
                print self.avg_time()
            return m
        else:
            self.a = float('-inf')
            self.b = float('inf')
           
            if time_remaining < 3:
                if self.time:
                    self.end_time = timeit.default_timer()
                    self.total_avg += (self.end_time - self.start_time)
                    print self.avg_time()
                return random.choice(moves)
            
            ordered_moves = []
            for move in moves:
                ordered_moves.append((move, self.short_utility(board, color, move)))

            sorted(ordered_moves, key=lambda x: x[1])

            new_moves = []
            new_moves = [move[0] for move in ordered_moves]

            moves = new_moves

            if self.move_num > 8:
                for move in moves:
                    if (move == (0, 0) or move == (0, 7) or move == (7, 0) or move == (7, 7)):
                        if self.time:
                            self.end_time = timeit.default_timer()
                            self.total_avg += (self.end_time - self.start_time)
                            print self.avg_time()
                        return move

            v = float('-inf')
            a = float('-inf')
            b = float('inf')
            if len(moves) > 18:
                for move in moves:
                    new_v = self.min_val_a_b(board, color, color, move, 3, time_remaining, a, b)
                    if new_v > v:
                        v = new_v
                        m = move
                    a = max(a, v)
                if self.time:
                    self.end_time = timeit.default_timer()
                    self.total_avg += (self.end_time - self.start_time)
                    print self.avg_time()
                return m
            else:
                for move in moves:
                    new_v = self.min_val_a_b(board, color, color, move, 3, time_remaining, a, b)
                    if new_v > v:
                        v = new_v
                        m = move
                    a = max(a, v)
                if self.time:
                    self.end_time = timeit.default_timer()
                    self.total_avg += (self.end_time - self.start_time)
                    print self.avg_time()
                return m
        

    def max_val(self, board, color, original_color, move, depth, time_remaining):
        time_spent = timeit.default_timer() - self.start_time

        if time_remaining - time_spent < 3:
            return move 
        
        newboard = deepcopy(board)
        newboard.execute_move(move, color)
        
        if self.log_boards:
            self.log_board(newboard)

        if self.terminal_test(newboard, color, depth):
            return self.utility(newboard, color, original_color, move)

        v = float('-inf')

        new_moves = newboard.get_legal_moves(color*-1)
        self.num_elem += 1
        self.num_nodes += len(new_moves)

        v = max(new_moves, key=lambda move: self.min_val(newboard, color*-1, original_color, move, depth-1, time_remaining))
		
        return v

    def min_val(self, board, color, original_color, move, depth, time_remaining):
        time_spent = timeit.default_timer() - self.start_time

        if time_remaining - time_spent < 3:
            return move
        
        newboard = deepcopy(board)
        newboard.execute_move(move, color)
        
        if self.log_boards:
            self.log_board(newboard)

        if self.terminal_test(newboard, color, depth):
            return self.utility(newboard, color, original_color, move)

        v = float('inf')

        new_moves = newboard.get_legal_moves(color*-1)
        self.num_elem += 1
        self.num_nodes += len(new_moves)

        v = min(new_moves, key=lambda move: self.max_val(newboard, color*-1, original_color, move, depth-1, time_remaining))

        return v

    def max_val_a_b(self, board, color, original_color, move, depth, time_remaining, a, b):
        time_spent = timeit.default_timer() - self.start_time

        # make random move when low on time
        if time_remaining - time_spent < 2:
            return move 

        newboard = deepcopy(board)
        newboard.execute_move(move, color)
        
        if self.log_boards:
            self.log_board(newboard)

        if self.terminal_test(newboard, color, depth):
            return self.utility(newboard, color, original_color, move)

        # reorder moves based on board positioning
        new_moves = newboard.get_legal_moves(color*-1)
        self.num_elem += 1
        self.num_nodes += len(new_moves)

        v = float('-inf')
        ordered_moves = []
        for move in new_moves:
            ordered_moves.append((move, self.short_utility(board, color, move)))

        sorted(ordered_moves, key=lambda x: x[1])

        new_moves = []
        new_moves = [move[0] for move in ordered_moves]
        
        for move in new_moves:
            v = max(v, self.min_val_a_b(newboard, color*-1, original_color, move, depth-1, time_remaining, a, b))
            if v >= b:
                return v
            a = max(a, v)
		
        return v 

    def min_val_a_b(self, board, color, original_color, move, depth, time_remaining, a, b):
        time_spent = timeit.default_timer() - self.start_time

        if time_remaining - time_spent < 2:
            return move 
        newboard = deepcopy(board)
        newboard.execute_move(move, color)
        
        if self.log_boards:
            self.log_board(newboard)

        if self.terminal_test(newboard, color, depth):
            return self.utility(newboard, color, original_color, move)

        new_moves = newboard.get_legal_moves(color*-1)
        self.num_elem += 1
        self.num_nodes += len(new_moves)
        
        v = float('inf')
        ordered_moves = []
        for move in new_moves:
            ordered_moves.append((move, self.short_utility(board, color, move)))

        sorted(ordered_moves, key=lambda x: x[1], reverse=True)

        new_moves = []
        new_moves = [move[0] for move in ordered_moves]
        
        for move in new_moves:
            v = min(v, self.max_val_a_b(newboard, color*-1, original_color, move, depth-1, time_remaining, a, b))
            if v <= a:
                return v
            b = min(b, v)
        
        return v 

    def stableness(self, board, piece):
        orig_x, orig_y = piece[1], piece[0]
        color = board[orig_x][orig_y]
       
        # -1 means unstable, 1 means stable

        # flanked from top
        x, y = orig_x, orig_y
        if y > 0 and board[x][y-1] == color*-1:
            while y+1 < 7 and board[x][y+1] == color:
                y += 1
            if y < 7 and board[x][y+1] == 0:
                return -1

        # flanked from bottom 
        x, y = orig_x, orig_y
        if y < 7 and board[x][y+1] == color*-1:
            while y-1 > 0 and board[x][y-1] == color:
                y -= 1
            if y > 0 and board[x][y-1] == 0:
                return -1

        # flanked from left
        x, y = orig_x, orig_y
        if x > 0 and board[x-1][y] == color*-1:
            while x+1 < 7 and board[x+1][y] == color:
                x += 1
            if x < 7 and board[x+1][y] == 0:
                return -1

        # flanked from right
        x, y = orig_x, orig_y
        if x < 7 and board[x+1][y] == color*-1:
            while x-1 > 0 and board[x-1][y] == color:
                x -= 1
            if x > 0 and board[x-1][y] == 0:
                return -1

        # flanked from left/top
        x, y = orig_x, orig_y
        if x > 0 and y > 0 and board[x-1][y-1] == color*-1:
            while x+1 < 7 and y+1 < 7 and board[x+1][y+1] == color:
                x += 1
                y += 1
            if x < 7 and y < 7 and board[x+1][y+1] == 0:
                return -1

        # flanked from left/bottom
        x, y = orig_x, orig_y
        if x > 0 and y < 7 and board[x-1][y+1] == color*-1:
            while x+1 < 7 and y-1 > 0 and board[x+1][y-1] == color:
                x += 1
                y -= 1
            if x < 7 and y > 0 and board[x+1][y-1] == 0:
                return -1

        # flanked from right/bottom
        x, y = orig_x, orig_y
        if x < 7 and y < 7 and board[x+1][y+1] == color*-1:
            while x-1 > 0 and y-1 > 0 and board[x-1][y-1] == color:
                x -= 1
                y -= 1
            if x > 0 and y > 0 and board[x-1][y-1] == 0:
                return -1

        # flanked from right/top
        x, y = orig_x, orig_y
        if x < 7 and y > 0 and board[x+1][y-1] == color*-1:
            while x-1 > 0 and y+1 < 7 and board[x-1][y+1] == color:
                x -= 1
                y += 1
            if x > 0 and y < 7 and board[x-1][y+1] == 0:
                return -1

        return 1

    def short_utility(self, board, original_color, move):
        pos_value = [[150, -15, 15, 10, 10, 15, -15, 150],
            [-15, -24, -6, -3, -3, -6, -24, -15],
            [15, -6, 8, 5, 5, 8, -6, 15],
            [10, -3, 5, 0, 0, 5, -3, 10],
            [10, -3, 5, 0, 0, 5, -3, 10],
            [15, -6, 8, 5, 5, 8, -6, 15],
            [-15, -24, -6, -3, -3, -6, -24, -15],
            [150, -15, 15, 10, 10, 15, -15, 150]]
        
        pos = 0
        pos += pos_value[move[1]][move[0]]

        return pos

    def utility(self, board, color, original_color, move, print_utility=False):
        """ Utility function. Heuristic based on positioning, stability, 
        and early in the game, mobility. """
        pos_value = [[150, -15, 15, 10, 10, 15, -15, 150],
            [-15, -24, -6, -3, -3, -6, -24, -15],
            [15, -6, 8, 5, 5, 8, -6, 15],
            [10, -3, 5, 0, 0, 5, -3, 10],
            [10, -3, 5, 0, 0, 5, -3, 10],
            [15, -6, 8, 5, 5, 8, -6, 15],
            [-15, -24, -6, -3, -3, -6, -24, -15],
            [150, -15, 15, 10, 10, 15, -15, 150]]
        
        h = 0

        if self.move_num < 7:
            num_moves_me = len(board.get_legal_moves(original_color))
            num_moves_op = len(board.get_legal_moves(original_color*-1))

            mobility = num_moves_me - num_moves_op

            h = 13*mobility
        elif self.move_num < 9:
            num_moves_me = len(board.get_legal_moves(original_color))
            num_moves_op = len(board.get_legal_moves(original_color*-1))

            mobility = num_moves_me - num_moves_op

            h = 9*mobility
            
        pieces_op = board.get_squares(original_color*-1)
        pieces_me = board.get_squares(original_color)

        stableness_me, stableness_op = 0, 0
        for piece in pieces_me:
            stableness_me += self.stableness(board, piece) * pos_value[piece[1]][piece[0]]
        
        for piece in pieces_op:
            stableness_op -= self.stableness(board, piece) * pos_value[piece[1]][piece[0]]

        s = float(stableness_me) / len(pieces_me) - float(stableness_op) / len(pieces_op)
        
        pos = 0
        if color == original_color:
            pos += pos_value[move[1]][move[0]]
        else:
            pos -= pos_value[move[1]][move[0]]

        h += 50*s + 5*pos
        
        if print_utility:
            print "%.2f + %i + %i" % (h, 50*s, 1*pos)
        return h


    def terminal_test(self, board, color, depth):
        if depth == 0:
            return True
        # game is over when all spaces filled
        if (abs(board.count(color)) + abs(board.count(color*-1))) == 64:
            return True
        if not board.get_legal_moves(color) or not board.get_legal_moves(color*-1):
            return True
        return False

    ################################################################
    # Extra functions used for Part 2: The Comparison Experiments  #
    ################################################################
    def log_board(self, board):
        d = self.board_as_string(board)
        if d in self.boards_seen:
            self.boards_seen[d] += 1
        else:
            self.boards_seen[d] = 1

    def board_as_string(self, board):
        d = list('.'*64)
        i = 0
        for y in range(7,-1,-1):
            for x in range(8):
                piece = board[x][y]
                if piece == -1: 
                    d[i] = 'B'
                elif piece == 1: 
                    d[i] = 'W'
                i += 1
        return ''.join(d)

    def get_duplicates_count(self):
        c = 0
        for b in self.boards_seen:
            if self.boards_seen[b] > 1:
                c += (self.boards_seen[b] - 1)
        return "Duplicates: %s" % c

    def avg_time(self):
        return "Average move time: %s" % (self.total_avg / float(self.move_num))

engine = StudentEngine
