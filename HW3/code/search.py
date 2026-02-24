# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in search_agents.py).
"""

from builtins import object
import util
import os

# (you can ignore this, although it might be helpful to know about)
# This is effectively an abstract class
# it should give you an idea of what methods will be available on problem-objects
class SearchProblem(object):
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem.
        """
        util.raise_not_defined()

    def is_goal_state(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raise_not_defined()

    def is_wall(self, state):
        """
          state: Search state

        Returns True if and only if the state is a wall.
        """
        util.raise_not_defined()


    def get_successors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, step_cost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'step_cost' is
        the incremental cost of expanding to that successor.
        """
        util.raise_not_defined()

    def get_cost_of_actions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raise_not_defined()


def tiny_maze_search(problem):
    """
    Returns a sequence of moves that solves tiny_maze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tiny_maze.
    """
    from game import Directions

    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depth_first_search(problem, initial_hit=0, return_hit=False):
    """Search the deepest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Stack

    # Initialize with (state, hitWalls, actions)
    stack = Stack()
    stack.push((problem.get_start_state(), [], initial_hit))  # (state, path, wall_hits)
    visited = set()
    visited.add((problem.get_start_state(), initial_hit))

    while not stack.is_empty():
        state, path, wall_hits = stack.pop()

        if wall_hits > 2:
            continue
        #print(state, wall_hits)
        if problem.is_goal_state(state) and (2>=wall_hits >= 1):
            if return_hit:
                return path, wall_hits - initial_hit
            else:
                return path

        for successor, action, cost in problem.get_successors(state):
                next_wall_hits = wall_hits + 1 if problem.is_wall(successor) else wall_hits
                nextState = (successor, next_wall_hits)
                if (nextState[0], nextState[1]) not in visited:
                    stack.push((nextState[0], path + [action], nextState[1]))
                    visited.add((nextState[0], nextState[1]))


    return []



def breadth_first_search(problem, initial_hit = 0, return_hit = False):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue

    queue = Queue()
    queue.push((problem.get_start_state(), [], initial_hit))
    visited = set()

    while not queue.is_empty():
        state, path, wall_hits = queue.pop()

        if wall_hits > 2:
            continue

        if problem.is_goal_state(state) and (2>= wall_hits >=1):
            if return_hit:
                return path, wall_hits - initial_hit
            else:
                return path


        for successor, action, _ in problem.get_successors(state):
            next_wall_hits = wall_hits + 1 if problem.is_wall(successor) else wall_hits
            nextState = (successor, next_wall_hits)
            if (nextState[0], nextState[1]) not in visited:
                queue.push((nextState[0], path + [action], nextState[1]))
                visited.add((nextState[0], nextState[1]))
    return []

def uniform_cost_search(problem, heuristic=None, initial_hit = 0, return_hit = False):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue

    pq = PriorityQueue()
    startState = problem.get_start_state()
    pq.push((startState, initial_hit, []), 0)

    visited = set()
    visited.add((startState, initial_hit))
    distance = {}
    distance[(startState, initial_hit)] = 0

    while True:
        if pq.is_empty():
            return []

        currentState, hitWalls, currentActions = pq.pop()

        if hitWalls > 2:
            continue

        if problem.is_goal_state(currentState) and (1 <= hitWalls <= 2):
            if return_hit:
                return currentActions, wall_hits - initial_hit
            else:
                return currentActions


        for successor, action, stepCost in problem.get_successors(currentState):
            if problem.is_wall(successor):
                nextState = (successor, hitWalls + 1)
            else:
                nextState = (successor, hitWalls)

            newActions = currentActions + [action]
            newCost = problem.get_cost_of_actions(newActions)
            if (nextState[0], nextState[1]) not in distance or newCost < distance[(nextState[0], nextState[1])]:
                pq.push((nextState[0], nextState[1], newActions), newCost)
                distance[(nextState[0], nextState[1])] = newCost


    return []

#
# heuristics
#
def a_really_really_bad_heuristic(position, problem):
    from random import random, sample, choices
    return int(random()*1000)

def null_heuristic(state, problem=None):
    return 0

def your_heuristic(state, problem=None):
    """ Your Custom Heuristic """
    "*** YOUR CODE HERE ***"
    return 0

def a_star_search(problem, heuristic=null_heuristic, initial_hit = 0, return_hit = False):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #util.raise_not_defined()
    from util import PriorityQueue

    pq = PriorityQueue()
    startState = problem.get_start_state()
    pq.push((startState, initial_hit, []), heuristic(startState, problem))

    visited = set()
    visited.add((startState, initial_hit))

    while True:
        if pq.is_empty():
            return []

        currentState, hitWalls, currentActions = pq.pop()

        if hitWalls > 2:
            continue

        if problem.is_goal_state(currentState) and (1 <= hitWalls <= 2):
            if return_hit:
                return currentActions, wall_hits - initial_hit
            else:
                return currentActions

        for successor, action, stepCost in problem.get_successors(currentState):
            if problem.is_wall(successor):
                nextState = (successor, hitWalls + 1)
            else:
                nextState = (successor, hitWalls)

            if (nextState[0], nextState[1]) not in visited:
                newActions = currentActions + [action]
                g_n = problem.get_cost_of_actions(newActions)
                h_n = heuristic(nextState[0], problem)
                f_n = g_n + h_n
                pq.push((nextState[0], nextState[1], newActions), f_n)
                visited.add((nextState[0], nextState[1]))

    return []


# Abbreviations
bfs   = breadth_first_search
dfs   = depth_first_search
astar = a_star_search
ucs   = uniform_cost_search
