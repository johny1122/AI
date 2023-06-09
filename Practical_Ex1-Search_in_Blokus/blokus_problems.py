from board import Board
from search import SearchProblem, ucs, Node
import util


class BlokusFillProblem(SearchProblem):
    """
    A one-player Blokus game as a search problem.
    This problem is implemented for you. You should NOT change it!
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.expanded = 0

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        """
        state: Search state
        Returns True if and only if the state is a valid goal state
        """
        return not any(state.pieces[0])

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, 1) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)


#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################
class BlokusCornersProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.expanded = 0
        "*** YOUR CODE HERE ***"
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state: Board):
        "*** YOUR CODE HERE ***"
        return (state.get_position(0, 0) == 0) and \
               (state.get_position(self.board.board_w - 1, 0) == 0) and \
               (state.get_position(0, self.board.board_h - 1) == 0) and \
               (state.get_position(self.board.board_w - 1, self.board.board_h - 1) == 0)

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in
                state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        "*** YOUR CODE HERE ***"
        total_tiles_used = 0
        for action in actions:
            total_tiles_used += action.piece.get_num_tiles()
        return total_tiles_used


def euclidian_distance(point1, point2):
    xy1 = point1
    xy2 = point2
    return ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** 0.5


def blokus_corners_heuristic(state: Board, problem):
    """
    Your heuristic for the BlokusCornersProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come up
    with an admissible heuristic; almost all admissible heuristics will be consistent
    as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the other hand,
    inadmissible or inconsistent heuristics may find optimal solutions, so be careful.
    """
    "*** YOUR CODE HERE ***"
    num_unvisited_corners = state.get_position(0, state.board_w - 1) + state.get_position(
        state.board_h - 1, 0) + state.get_position(state.board_h - 1, state.board_w - 1)

    unused_pieces = []
    for piece_id in range(state.piece_list.get_num_pieces()):
        if state.pieces[0, piece_id] == 1:  # piece is unused
            max_dimension = max(state.board_w, state.board_h)
            unused_pieces.append(state.piece_list.get_piece(piece_id).get_num_tiles() + max_dimension)
    unused_pieces.sort()

    sum_tiles = 0
    for i in range(0, len(unused_pieces) - num_unvisited_corners - 3):  # remove the biggest pieces from sum
        sum_tiles += unused_pieces[i]
    return sum_tiles


class BlokusCoverProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=[(0, 0)]):
        self.targets = targets.copy()
        self.expanded = 0
        "*** YOUR CODE HERE ***"
        self.num_of_targets = len(targets)
        self.starting_point = starting_point
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.board_size = board_h * board_w

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state: Board):
        "*** YOUR CODE HERE ***"
        for target in self.targets:
            if state.get_position(target[1], target[0]) != 0:
                return False

        return True

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in
                state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        "*** YOUR CODE HERE ***"
        total_tiles_used = 0
        for action in actions:
            total_tiles_used += action.piece.get_num_tiles()
        return total_tiles_used


def most_far_target(state: Board, problem):
    unvisited_targets_num = 0
    max_distance = 0
    for target in problem.targets:
        if state.state[target] == -1:
            unvisited_targets_num += 1
            curr_distance = euclidian_distance(problem.starting_point, target)

            if curr_distance > max_distance:
                max_distance = curr_distance
    return max_distance, unvisited_targets_num


def find_unused_pieces(state: Board, unvisited_targets_num):
    pieces_sizes = []
    for piece_id in range(state.piece_list.get_num_pieces()):
        if state.pieces[0, piece_id]:  # piece is unused
            pieces_sizes.append(state.piece_list.get_piece(piece_id).get_num_tiles())
            unvisited_targets_num -= 1
            if unvisited_targets_num == 0:  # found all pieces
                break
    return pieces_sizes


def sum_tiles_to_use(unvisited_targets_num, pieces_sizes, max_distance):
    sum_tiles = 0
    for piece_index in range(min(unvisited_targets_num, len(pieces_sizes))):
        sum_tiles += pieces_sizes[piece_index]
        if sum_tiles >= max_distance:
            if unvisited_targets_num < 2:
                return pieces_sizes[0]
            else:
                return sum_tiles
    return sum_tiles


def blokus_cover_heuristic(state: Board, problem: BlokusCoverProblem):
    "*** YOUR CODE HERE ***"
    max_distance, unvisited_targets_num = most_far_target(state, problem)
    pieces_sizes = find_unused_pieces(state, unvisited_targets_num)
    pieces_sizes = sorted(pieces_sizes[:min(len(pieces_sizes), problem.num_of_targets)])
    return sum_tiles_to_use(unvisited_targets_num, pieces_sizes, max_distance)


class ClosestLocationSearch:
    """
    In this problem you have to cover all given positions on the board,
    but the objective is speed, not optimality.
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=(0, 0)):
        self.expanded = 0
        self.targets = targets.copy()
        "*** YOUR CODE HERE ***"
        self.starting_point = starting_point
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.num_of_targets = len(targets)

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def solve(self):
        """
        This method should return a sequence of actions that covers all target locations on the board.
        This time we trade optimality for speed.
        Therefore, your agent should try and cover one target location at a time. Each time, aiming for the closest uncovered location.
        You may define helpful functions as you wish.

        Probably a good way to start, would be something like this --

        current_state = self.board.__copy__()
        backtrace = []

        while ....

            actions = set of actions that covers the closets uncovered target location
            add actions to backtrace

        return backtrace
        """
        "*** YOUR CODE HERE ***"
        current_state = self.board.__copy__()
        backtrace = []

        # if there are no targets  or  there is one target same as starting point  ->  no moves necessary
        if (not self.targets) or (self.num_of_targets == 1 and self.starting_point == self.targets[0]):
            return []

        # keep track of targets ordered by min distance to them
        unvisited_targets = util.PriorityQueue()
        for target in self.targets:
            unvisited_targets.push(target, euclidian_distance(self.starting_point, target))

        while not unvisited_targets.isEmpty():
            closest_target = unvisited_targets.pop()  # get the closest target
            sub_problem = SubProblem(current_state, closest_target)
            moves_to_target = ucs(sub_problem)  # find best moves

            backtrace += moves_to_target
            for move in moves_to_target:
                current_state = current_state.do_move(0, move)
            self.expanded += sub_problem.expanded

        return backtrace


class SubProblem(SearchProblem):
    def __init__(self, state: Board, target=(0, 0)):
        self.expanded = 0
        self.state = state
        self.target = target

    def get_start_state(self):
        return self.state

    def is_goal_state(self, state: Board):
        if state.get_position(self.target[1], self.target[0]) != 0:
            return False
        return True

    def get_successors(self, state):
        self.expanded += 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in
                state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        total_tiles_used = 0
        for action in actions:
            total_tiles_used += action.piece.get_num_tiles()
        return total_tiles_used


class MiniContestSearch:
    """
    Implement your contest entry here
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=(0, 0)):
        self.targets = targets.copy()
        "*** YOUR CODE HERE ***"

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def solve(self):
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()
