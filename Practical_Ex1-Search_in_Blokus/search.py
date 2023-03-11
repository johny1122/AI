"""
In search.py, you will implement generic search algorithms
"""

import util


class Node:

    def __init__(self, state, path_to_node, path_cost):
        self.state = state
        self.path_to_node = path_to_node
        self.path_cost = path_cost


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def get_cost_of_actions(self, actions) -> int:
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def depth_first_search(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

	print("Start:", problem.get_start_state().state)
    print("Is the start a goal?", problem.is_goal_state(problem.get_start_state()))
    print("Start's successors:", problem.get_successors(problem.get_start_state()))
    """
    "*** YOUR CODE HERE ***"
    fringe = util.Stack()
    init_node = Node(problem.get_start_state(), [], 0)
    fringe.push(init_node)
    visited = set()

    while not fringe.isEmpty():
        current_node = fringe.pop()
        if problem.is_goal_state(current_node.state):
            return current_node.path_to_node

        if current_node.state not in visited:
            successors = problem.get_successors(current_node.state)
            for child_triple in successors:
                child_state, child_move, child_cost = child_triple
                child_node = Node(child_state, current_node.path_to_node + [child_move],
                                  current_node.path_cost + child_cost)
                fringe.push(child_node)
            visited.add(current_node.state)

    return []  # if root has no children


def breadth_first_search(problem: SearchProblem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    fringe = util.Queue()
    init_node = Node(problem.get_start_state(), [], 0)
    fringe.push(init_node)
    visited = set()

    while not fringe.isEmpty():
        current_node = fringe.pop()
        if problem.is_goal_state(current_node.state):
            return current_node.path_to_node

        if current_node.state not in visited:
            successors = problem.get_successors(current_node.state)
            for child_triple in successors:
                child_state, child_move, child_cost = child_triple
                child_node = Node(child_state, current_node.path_to_node + [child_move],
                                  current_node.path_cost + child_cost)
                fringe.push(child_node)
            visited.add(current_node.state)

    return []  # if root has no children


def uniform_cost_search(problem: SearchProblem):
    """
    Search the node of least total cost first.
    """
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()
    init_node = Node(problem.get_start_state(), [], 0)
    fringe.push(init_node, 0)
    visited = set()

    while not fringe.isEmpty():
        current_node = fringe.pop()
        if problem.is_goal_state(current_node.state):
            return current_node.path_to_node

        if current_node.state not in visited:
            successors = problem.get_successors(current_node.state)
            for child_triple in successors:
                child_state, child_move, child_cost = child_triple
                child_node = Node(child_state, current_node.path_to_node + [child_move],
                                  current_node.path_cost + child_cost)
                fringe.push(child_node, child_node.path_cost)
            visited.add(current_node.state)

    return []  # if root has no children


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def a_star_search(problem: SearchProblem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()
    init_node = Node(problem.get_start_state(), [], 0)
    fringe.push(init_node, 0)
    visited = set()

    while not fringe.isEmpty():
        current_node = fringe.pop()
        if problem.is_goal_state(current_node.state):
            return current_node.path_to_node

        if current_node.state not in visited:
            successors = problem.get_successors(current_node.state)
            for child_triple in successors:
                child_state, child_move, child_cost = child_triple
                child_node = Node(child_state, current_node.path_to_node + [child_move],
                                  current_node.path_cost + child_cost)
                fringe.push(child_node, child_node.path_cost + heuristic(child_node.state, problem))
            visited.add(current_node.state)

    return []  # if root has no children

# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
