#__author__ = "Ziyuan Li"
#__ID__ = zl2824


from __future__ import division
from __future__ import print_function

import resource
import sys
import math
import time
import queue as Q
from collections import deque

goal_state_config = [0,1,2,3,4,5,6,7,8]
nodes_expanded = 0
path_action = []
search_depth = 0
max_search_depth = 0
cost_of_path = 0
board_size = 0
expanded = set()


#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    
    
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])

def move_up(initial_state):
    global board_size
    new_state = PuzzleState(initial_state.config[:], board_size,initial_state,"Initial",initial_state.cost)
    pos = initial_state.config.index(0)
    if pos in (0,1,2):
        return None
    else:
        new_state.config[pos],new_state.config[pos-3] = new_state.config[pos-3],new_state.config[pos]
        new_state.parent = initial_state
        new_state.action = "Up"
        new_state.cost += 1
    return new_state

def move_down(initial_state):
    global board_size
    new_state = PuzzleState(initial_state.config[:], board_size,initial_state,"Initial",initial_state.cost)
    pos = initial_state.config.index(0)
    if pos in (6,7,8):
        return None
    else:
        new_state.config[pos],new_state.config[pos+3] = new_state.config[pos+3],new_state.config[pos]
        new_state.parent = initial_state
        new_state.action = "Down"
        new_state.cost += 1
    return new_state

def move_left(initial_state):
    global board_size
    new_state = PuzzleState(initial_state.config[:], board_size,initial_state,"Initial",initial_state.cost)
    pos = initial_state.config.index(0)
    if pos in (0,3,6):
        return None
    else:
        new_state.config[pos],new_state.config[pos-1] = new_state.config[pos-1],new_state.config[pos]
        new_state.parent = initial_state
        new_state.action = "Left"
        new_state.cost += 1
        return new_state


def move_right(initial_state):
    global board_size
    new_state = PuzzleState(initial_state.config[:], board_size,initial_state,"Initial",initial_state.cost)
    pos = initial_state.config.index(0)
    if pos in (2,5,8):
        return None
    else:
        new_state.config[pos],new_state.config[pos+1] = new_state.config[pos+1],new_state.config[pos]
        new_state.parent = initial_state
        new_state.action = "Right"
        new_state.cost += 1
        return new_state

def expand(initial_state):
    """ Generate the child nodes of this node """
    global nodes_expanded
    nodes_expanded += 1
        # Add child nodes in order of UDLR
    children = [
        move_up(initial_state),
        move_down(initial_state),
        move_left(initial_state),
        move_right(initial_state)]

        # Compose self.children of all non-None children states
    initial_state.children = [state for state in children if state is not None]
    return initial_state.children


def arrange(state):
    arrange = map(str, state.config) 
    arrange = ''.join(arrange)
    return arrange

# Function that Writes to output.txt
def writeOutput():
    global goal_state,path_action,cost_of_path,nodes_expanded,search_depth,max_search_depth,running_time,max_ram_usage
    find_path(goal_state)
    search_depth = cost_of_path
    file = open("output.txt", "w")
    file.write("path_to_goal: " + str(path_action) + "\n")
    file.write("cost_of_path: " + str(cost_of_path) + "\n")
    file.write("nodes_expanded: " + str(nodes_expanded) + "\n")
    file.write("search_depth: " + str(search_depth) + "\n")
    file.write("max_search_depth: " + str(max_search_depth) + "\n")
    file.write("running_time: " + str(running_time) + "\n")
    file.write("max_ram_usage: " + str(max_ram_usage) + "\n")



def bfs_search(initial_state):

    global goal_state_config,goal_state,max_search_depth
    
    frontier = deque([])
    frontier_config = set()
    frontier.append(initial_state)
    frontier_config.add(arrange(initial_state))
    explored = set()

    while len(frontier)!= 0:
        state = frontier.popleft()
        explored.add(arrange(state))

        if test_goal(state):
            goal_state = state
            print("Solution found!")
            return goal_state

        neighbors = expand(state)
        
        for neighbor in neighbors:
            if arrange(neighbor) not in explored:
                if arrange(neighbor) not in frontier_config:
                    frontier.append(neighbor)
                    frontier_config.add(arrange(neighbor))

                if neighbor.cost > max_search_depth:
                    max_search_depth = neighbor.cost

    return False
    

def dfs_search(initial_state):
    global goal_state_config,goal_state,max_search_depth
    
    frontier = []
    frontier_config = set()
    frontier.append(initial_state)
    frontier_config.add(arrange(initial_state))
    explored = set()

    while len(frontier)!= 0:
        state = frontier.pop()
        explored.add(arrange(state))

        if test_goal(state):
            goal_state = state
            print("Solution found!")
            return goal_state

        neighbors_reverse = expand(state)
        neighbors = list(reversed(neighbors_reverse))

        for neighbor in neighbors:
            if arrange(neighbor) not in explored:
                if arrange(neighbor) not in frontier_config:
                    frontier.append(neighbor)
                    frontier_config.add(arrange(neighbor))

                    if neighbor.cost > max_search_depth:
                        max_search_depth = neighbor.cost

    return False

def A_star_search(initial_state):
    global goal_state_config,goal_state,max_search_depth, board_size
    h = calculate_manhattan_dist(initial_state)
    initial_state_key = h
    frontier = Q.PriorityQueue()
    frontier_config = set()
    explored = set()
    count = 0

    frontier.put((initial_state_key, 0, count,initial_state))
    count +=1
    frontier_config.add(arrange(initial_state))

    while not frontier.empty():
        a = frontier.get()
        state = a[3]
        explored.add(arrange(state))

        if test_goal(state):
            goal_state = state
            print("Solution found!")
            return goal_state

        neighbors = expand(state)

        for neighbor in neighbors:
            if arrange(neighbor) not in explored:
                if arrange(neighbor) not in frontier_config:
                    neighbor_h = calculate_manhattan_dist(neighbor)
                    neighbor_key = neighbor.cost + neighbor_h
                    neighbor_move = movement(neighbor)
                    frontier.put((neighbor_key,neighbor_move,count,neighbor))
                    count+=1
                    frontier_config.add(arrange(neighbor))

                    if neighbor.cost > max_search_depth:
                        max_search_depth = neighbor.cost
                #no need to decrease keys here

    return False

def movement(state):
    if state.action == "Up":
        a = 1
    elif state.action == "Down":
        a = 2
    elif state.action == "Left":
        a = 3
    elif state.action == "Right":
        a = 4

    return a

def find_path(state):
    global path_found,path_action,cost_of_path
    path_found_reverse = list()
    path_found_reverse.append(state)
    while state.parent is not None:
        path_found_reverse.append(state.parent)
        state = state.parent
    path_found = list(reversed(path_found_reverse))
    for actions in path_found:
        if actions.action != "Initial":
            path_action.append(actions.action)
    cost_of_path = len(path_action)



def calculate_manhattan_dist(state):
    global board_size

    manhattan_dist = 0
    for i in range(1,9):
        pos1 = state.config.index(i) // board_size
        pos2 = state.config.index(i) % board_size
        goal_pos1 = i // board_size
        goal_pos2 = i % board_size
        distance = (abs(pos1-goal_pos1) + abs(pos2-goal_pos2))
        manhattan_dist += distance
    return manhattan_dist
    

def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    global goal_state_config
    if puzzle_state.config == goal_state_config:
       return True
    else:
        return False

# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    global board_size,running_time,max_ram_usage
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()

    if   search_mode == "bfs": bfs_search(hard_state)
    elif search_mode == "dfs": dfs_search(hard_state)
    elif search_mode == "ast": A_star_search(hard_state)
    else:
        print("Enter valid command arguments !")

    end_time = time.time()
    running_time = end_time-start_time
    running_time = format(running_time, '.8f')
    max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    max_ram_usage = format(max_ram_usage/1000000, '.8f')


    writeOutput()

    

if __name__ == '__main__':
    main()
