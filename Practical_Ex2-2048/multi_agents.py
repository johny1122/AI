import math

import numpy as np
import abc
import util
from game import Agent, Action
from game_state import GameState

MAX = 0
MIN = 1


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def get_action(self, game_state):
        """
        You do not need to change this method, but you're welcome to.

        get_action chooses among the best options according to the evaluation function.

        get_action takes a game_state and returns some Action.X for some X in the set {UP, DOWN, LEFT, RIGHT, STOP}
        """

        # Collect legal moves and successor states
        legal_moves = game_state.get_agent_legal_actions()

        # Choose one of the best actions
        scores = [self.evaluation_function(game_state, action) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = np.random.choice(best_indices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legal_moves[chosen_index]

    def evaluation_function(self, current_game_state: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (GameState.py) and returns a number, where higher numbers are better.

        """

        # Useful information you can extract from a GameState (game_state.py)

        successor_game_state = current_game_state.generate_successor(action=action)
        board = successor_game_state.board
        max_tile = successor_game_state.max_tile
        score = successor_game_state.score

        "*** YOUR CODE HERE ***"
        empty_tiles = len(successor_game_state.get_empty_tiles()[0])
        sum_of_corners_right = board[0, 0] + (board[0, 1] + board[1, 0]) + (board[1, 1] / 10)
        sum_of_corners_left = board[3, 0] + (board[3, 1] + board[2, 0]) + (board[2, 1] / 10)
        max_corners = max(sum_of_corners_left, sum_of_corners_right)
        sum_of_large_tiles = np.sum((board >= (max_tile / 4)))
        return (score / 4) + sum_of_large_tiles + (empty_tiles * 2) + (max_corners ** 2)


def score_evaluation_function(current_game_state):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return current_game_state.score


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinmaxAgent, AlphaBetaAgent & ExpectimaxAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evaluation_function='scoreEvaluationFunction', depth=2):
        self.evaluation_function = util.lookup(evaluation_function, globals())
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state):
        return


class MinmaxAgent(MultiAgentSearchAgent):

    def minimax_recursion(self, curr_depth, agent_turn, curr_state: GameState):
        if curr_depth == 0 or curr_state.done:  # reached a leaf  or  has no legal actions
            return self.evaluation_function(curr_state)

        children_scores = []
        actions_list = []
        for legal_action in curr_state.get_legal_actions(agent_turn):
            child_state = curr_state.generate_successor(agent_index=agent_turn, action=legal_action)
            if agent_turn == MAX:
                children_scores.append(self.minimax_recursion(curr_depth, MIN, child_state))
            else:  # MIN
                children_scores.append(self.minimax_recursion(curr_depth - 1, MAX, child_state))
            actions_list.append(legal_action)

        if agent_turn == MAX:
            if curr_depth == self.depth:  # root  ->  return action and not score
                max_score = max(children_scores)
                max_score_index = children_scores.index(max_score)
                return actions_list[max_score_index]  # return the best action to do now

            return max(children_scores, default=0)  # not root  ->  return max score

        else:  # MIN
            return min(children_scores, default=0)

    def get_action(self, game_state: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        game_state.get_legal_actions(agent_index):
            Returns a list of legal actions for an agent
            agent_index=0 means our agent, the opponent is agent_index=1

        Action.STOP:
            The stop direction, which is always legal

        game_state.generate_successor(agent_index, action):
            Returns the successor game state after an agent takes an action
        """
        """*** YOUR CODE HERE ***"""
        return self.minimax_recursion(self.depth, MAX, game_state)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def alpha_beta_recursion(self, curr_depth, agent_turn, curr_state: GameState, alpha, beta):
        if curr_depth == 0 or curr_state.done:  # reached a leaf  or  has no legal actions
            return self.evaluation_function(curr_state)

        if agent_turn == MAX:
            actions_list = []
            children_scores = []
            max_score = 0
            for legal_action in curr_state.get_legal_actions(agent_turn):
                child_state = curr_state.generate_successor(agent_index=agent_turn, action=legal_action)
                curr_score = self.alpha_beta_recursion(curr_depth, MIN, child_state, alpha, beta)
                max_score = max(max_score, curr_score)
                alpha = max(alpha, curr_score)
                if beta <= alpha:
                    break
                actions_list.append(legal_action)
                children_scores.append(curr_score)

            if curr_depth == self.depth:  # root  ->  return action and not score
                max_score_index = children_scores.index(max_score)
                return actions_list[max_score_index]  # return the best action to do now

            return max_score  # not root  ->  return max score

        else:  # MIN
            min_score = math.inf
            for legal_action in curr_state.get_legal_actions(agent_turn):
                child_state = curr_state.generate_successor(agent_index=agent_turn, action=legal_action)
                curr_score = self.alpha_beta_recursion(curr_depth - 1, MAX, child_state, alpha, beta)
                min_score = min(min_score, curr_score)
                beta = min(beta, curr_score)
                if beta <= alpha:
                    break

            return min_score

    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        """*** YOUR CODE HERE ***"""
        return self.alpha_beta_recursion(self.depth, MAX, game_state, -math.inf, math.inf)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def expectimax_recursion(self, curr_depth, agent_turn, curr_state: GameState):
        if curr_depth == 0 or curr_state.done:  # reached a leaf  or  has no legal actions
            return self.evaluation_function(curr_state)

        children_scores = []
        actions_list = []
        for legal_action in curr_state.get_legal_actions(agent_turn):
            child_state = curr_state.generate_successor(agent_index=agent_turn, action=legal_action)
            if agent_turn == MAX:
                children_scores.append(self.expectimax_recursion(curr_depth, MIN, child_state))
            else:  # MIN
                children_scores.append(self.expectimax_recursion(curr_depth - 1, MAX, child_state))
            actions_list.append(legal_action)

        if agent_turn == MAX:
            if curr_depth == self.depth:  # root  ->  return action and not score
                max_score = max(children_scores)
                max_score_index = children_scores.index(max_score)
                return actions_list[max_score_index]  # return the best action to do now

            return max(children_scores, default=0)  # not root  ->  return max score

        else:  # MIN
            return np.mean(children_scores)  # return average score (expectation with uniform probability)

    def get_action(self, game_state):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        The opponent should be modeled as choosing uniformly at random from their
        legal moves.
        """
        """*** YOUR CODE HERE ***"""
        return self.expectimax_recursion(self.depth, MAX, game_state)


def better_evaluation_function(current_game_state: GameState):
    """
    Your extreme 2048 evaluation function (question 5).

    DESCRIPTION: <write something here, so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    empty_tiles = len(current_game_state.get_empty_tiles()[0])
    board = current_game_state.board
    sum_of_corners_right = board[0, 0] + (board[0, 1] + board[1, 0]) + (board[1, 1] / 10)
    sum_of_corners_left = board[3, 0] + (board[3, 1] + board[2, 0]) + (board[2, 1] / 10)
    max_corners = max(sum_of_corners_left, sum_of_corners_right)
    sum_of_large_tiles = np.sum((board >= (current_game_state.max_tile / 4)))
    return (current_game_state.score / 4) + sum_of_large_tiles + (max_corners * 2) + (empty_tiles ** 2)


# Abbreviation
better = better_evaluation_function
