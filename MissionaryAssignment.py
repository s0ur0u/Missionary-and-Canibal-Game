# Definition of the different states
class State:
    def __init__(self, cannibals_west, missionaries_west, boat_side):
        self.cannibals_west = cannibals_west
        self.missionaries_west = missionaries_west
        self.boat_side = boat_side

# Evaluation of the valid states
    def is_valid(self):
        if self.cannibals_west < 0 or self.missionaries_west < 0:
            return False
        if self.cannibals_west > 3 or self.missionaries_west > 3:
            return False
        if self.cannibals_west > self.missionaries_west and self.missionaries_west > 0:
            return False
        if 3 - self.cannibals_west > 3 - self.missionaries_west and 3 - self.missionaries_west > 0:
            return False
        return True

#  checking if the current state is a goal state
    def is_goal(self):
        return self.cannibals_west == 0 and self.missionaries_west == 0

    def __eq__(self, other):
        return self.cannibals_west == other.cannibals_west and self.missionaries_west == other.missionaries_west and self.boat_side == other.boat_side
#    return of the hash value for the current state
    def __hash__(self):
        return hash((self.cannibals_west, self.missionaries_west, self.boat_side))
#   string representation of the current state
    def __str__(self):
        return f"On west bank: {self.missionaries_west} missionaries and {self.cannibals_west} cannibals. On East bank: {3-self.missionaries_west} missionaries and {3-self.cannibals_west} cannibals. Boat is on {'west' if self.boat_side == 0 else 'east'} side."

#   Definition of a node in the search tree
class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
#   Addition of children in the search tree
    def expand(self):
        children = []
        for delta_c, delta_m, delta_b in [(1, 0, 1), (2, 0, 1), (0, 1, 1), (0, 2, 1), (1, 1, 1)]:#List
    # of the different valid states on the east bank where the cannibals should not outnumber the missionaries
            if self.state.boat_side == 0:
                new_state = State(self.state.cannibals_west - delta_c, self.state.missionaries_west - delta_m, 1)
            else:
                new_state = State(self.state.cannibals_west + delta_c, self.state.missionaries_west + delta_m, 0)
            if new_state.is_valid():
                children.append(Node(new_state, self))
        return children
#   list of states that represent the solution path from the initial state to the goal state
    def get_path(self):
        path = []
        node = self
        while node is not None:
            path.append(node.state)
            node = node.parent
        return path[::-1]

# Implementation of the bfs algorithm
def breadth_first_search(initial_state):
    initial_node = Node(initial_state)
    if initial_node.state.is_goal():
        return initial_node.get_path()
    frontier = [initial_node]
    explored = set()
    while frontier:
        node = frontier.pop(0)
        if node.state.is_goal():
            return node.get_path()
        explored.add(node.state)
        children = node.expand()
        for child in children:
            if child.state not in explored and child not in frontier:
                frontier.append(child)
    return None


# Initial state: 3 cannibals and 3 missionaries on the west bank, boat is on the west side.
initial_state = State(3, 3, 0)

# Solve the problem using breadth-first search
solution_path = breadth_first_search(initial_state)
def print_solution_path(solution_path):
    if solution_path is None:
        print("No solution found!")
    else:
        print("Solution found:")
        for i, state in enumerate(solution_path):
            print(f"Step {i}: {state}")
        print(f"Step {len(solution_path)}: All missionaries and cannibals have crossed to the east bank.")


print_solution_path(solution_path)