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
from game import Directions, Actions

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


def first_hit(problem, start):
    # look all directions
    # if wall is adjacent hit it
    # turn around and go back to escape wall
    # finish searching algorithm
    # return wall_hit_action + normal_path


    # x, y = start
    # Direct = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]
    # Opp = [Directions.SOUTH, Directions.NORTH, Directions.WEST, Directions.EAST]
    # for direction, opposite in zip(Direct, Opp):
    #     if direction == Directions.NORTH:
    #         neighbor = (x, y + 1)
    #     elif direction == Directions.SOUTH:
    #         neighbor = (x, y - 1)
    #     elif direction == Directions.EAST:
    #         neighbor = (x + 1, y)
    #     elif direction == Directions.WEST:
    #         neighbor = (x - 1, y)

    #     if problem.is_wall(neighbor):
    #         return [direction, opposite]


    # return []

    # Extract position
    if isinstance(start, tuple) and len(start) > 0 and isinstance(start[0], tuple):
        x, y = start[0]   # Corners style: ((x,y), visited)
    else:
        x, y = start      # Position style: (x,y)

    pairs = [
        (Directions.NORTH, Directions.SOUTH),
        (Directions.SOUTH, Directions.NORTH),
        (Directions.EAST,  Directions.WEST),
        (Directions.WEST,  Directions.EAST),
    ]

    # We need a walls grid to check neighbors safely
    if not hasattr(problem, "walls"):
        return []

    for bonk_dir, opp_dir in pairs:
        dx, dy = Actions.direction_to_vector(bonk_dir)
        wx, wy = int(x + dx), int(y + dy)

        # adjacent wall => bonk direction found
        if problem.walls[wx][wy]:
            prefix = [bonk_dir]

            # only add opposite if it is a legal move (not a wall)
            odx, ody = Actions.direction_to_vector(opp_dir)
            ox, oy = int(x + odx), int(y + ody)
            if not problem.walls[ox][oy]:
                prefix.append(opp_dir)

            return prefix

    return []



def depth_first_search(problem):
    """Search the deepest nodes in the search tree first."""

    """important: problem.get_start_state(), problem.is_goal_state(state), 
    problem.get_successors(state) => returns a list of triples successor_state, 
    action (direction state), step_cost (DFS ignores this) """

    # implement a stack for LIFO ordering
    start = problem.get_start_state()
    
    if problem.is_goal_state(start):
        return []                               # start at food
    
    stack = util.Stack()
    visitedStates = set()
    stack.push((start, []))
    # wall_hit = first_hit(problem, start)
    # print("Wall hit action:", wall_hit)
    # print(problem.get_cost_of_actions(wall_hit))


    while not stack.is_empty():                                # while stack is not empty
        state, path = stack.pop()

        if state in visitedStates:
            continue

        visitedStates.add(state)
        if problem.is_goal_state(state):
            if problem.__class__.__name__ == "CornersProblem":
                return first_hit(problem, start) + path
            else:
                return path
        
        for (next_state, action, cost) in problem.get_successors(state):
            if next_state not in visitedStates and not problem.is_wall(next_state):
                stack.push((next_state, path + [action]))

    return []

def breadth_first_search(problem):
    """Search the shallowest nodes in the search tree first."""
    
    """important: problem.get_start_state(), problem.is_goal_state(state), 
    problem.get_successors(state) => returns a list of triples successor_state, 
    action (direction state), step_cost (DFS ignores this) """

    # implement a stack for FIFO ordering
    start = problem.get_start_state()

    if problem.is_goal_state(start):
        return []                                               # start at food
    
    queue = util.Queue()
    visitedStates = set()
    queue.push((start, []))
    
    while not queue.is_empty():                                 # while stack is not empty
        state, path = queue.pop()

        if state in visitedStates:                              # skip if visited
            continue

        visitedStates.add(state)                                # add to visited
        if problem.is_goal_state(state):                        # if this is food
            if problem.__class__.__name__ == "CornersProblem":
                return first_hit(problem, start) + path
            else:
                return path     
                                            # return path to food
        for (next_state, action, cost) in problem.get_successors(state):
            if next_state not in visitedStates and not problem.is_wall(next_state):     # if not wall or visited push!
                queue.push((next_state, path + [action]))

    return []


def uniform_cost_search(problem, heuristic=None):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # implement a stack for LIFO ordering
    start = problem.get_start_state()
    
    if problem.is_goal_state(start):
        return []                                               # start at food
    
    # state, actions, cost
    p_queue = util.PriorityQueue()
    p_queue.push((start, [], 0), 0)

    # lowest cost / goal to reach state
    lowest = {start: 0}
    
    while not p_queue.is_empty():                                 # while stack is not empty
        state, actions, cost = p_queue.pop()

        # if this entry is worse than our current entry
        if cost > lowest.get(state, float("inf")):                        # if this is food
            continue

        if problem.is_goal_state(state):
            if problem.__class__.__name__ == "CornersProblem":
                return first_hit(problem, start) + actions
            else:
                return actions
        
        # return path to food
        for (next_state, action, step_cost) in problem.get_successors(state):
            new_cost = cost + step_cost

            if new_cost < lowest.get(next_state, float("inf")) and not problem.is_wall(next_state):  
                lowest[next_state] = new_cost   
                p_queue.push((next_state, actions + [action], new_cost), new_cost)

    return []




# heuristics
    
def a_really_really_bad_heuristic(position, problem):
    from random import random, sample, choices
    return int(random()*1000)

def null_heuristic(state, problem=None):
    return 0

def your_heuristic(state, problem=None):
    """ Your Custom Heuristic """
    x, y = state
    gx, gy = problem.goal

    # logic from search_agents.py
    manhattan_heuristic = abs(x - gx) + abs(y - gy)
    euclidean_heuristic = ((x - gx) ** 2 + (y - gy) ** 2) ** 0.5

    return max(manhattan_heuristic, euclidean_heuristic) 
    
def a_star_search(problem, heuristic=your_heuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # get start position and see if start is end
    start = problem.get_start_state()
    if problem.is_goal_state(start):
        return []
    
    # now establish data structure PriorityQueue
    priority_queue = util.PriorityQueue()
    priority_queue.push((start, [], 0), 0 + heuristic(start, problem))

    # lowest cost path to goal, will be updated (DICTIONARY)
    best_path = {start: 0}

    while not priority_queue.is_empty():
        # get initial & prior information per iteration / move
        (state, path, g) = priority_queue.pop()

        # check if this path is worse than the previous
        if g > best_path[state]:
            continue

        # this will be used to check if we have reached our goal
        # it also prvoides one wall hit to pass
        if problem.is_goal_state(state):
            if problem.__class__.__name__ == "CornersProblem":
                return first_hit(problem, start) + path
            else:
                return path
                    
        # loop through each of the successor states to compare
        # cost will be used to compare with the lowest we have so far
        # and action will be used to update the path to be returned
        for (next_state, action, step_cost) in problem.get_successors(state):
            current_cost = g + step_cost
            
            # if this is a new state or of this cost is less than the best path to the next state
            if (next_state not in best_path or current_cost < best_path[next_state]) and not problem.is_wall(next_state):
                # add this node to the best_path dictionary 
                best_path[next_state] = current_cost
                new_path = path + [action]
                f = current_cost + heuristic(next_state, problem)

                # push this node onto queue 
                priority_queue.push((next_state, new_path, current_cost), f)

    
    return []       # simple no solution... Should never happen.


# Abbreviations
bfs   = breadth_first_search
dfs   = depth_first_search
astar = a_star_search
ucs   = uniform_cost_search
