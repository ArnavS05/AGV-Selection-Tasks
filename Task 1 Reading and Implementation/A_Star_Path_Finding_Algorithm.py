'''Assuming only vertical and horizontal movements from a position labelled 0
to another position labelled 0, only.

DESCRIPTION OF CLASSES:
Class Node:
It is used to store information of a particular position. It stores, g_cost, h_cost
and it has a property f_cost. Two nodes can be compared based on their f_cost as a result
of the implimentation of the dunder function __lt__. It also stores its parent which is the
node closest to it in the direction of start node.

Class A_Star:
This class is the main implementation of the A* path finding algorithm. It has a closed set
which has selected nodes as possible nodes in the path and an open set having all explored
nodes. The open set is kept sorted according to f_cost of the nodes by adding nodes to it
using the push_to_open function of this class. Time complexity of this function is O(logn).
pop_open function is used to return the least costly node from the open set. This class also
has functions to get valid neighbours of a node, get h_cost of a node, and find the final path
by iterating through nodes using their parents, untill start node is reached.
This class also has the main function named find_path, which implements the A* algorithm.

At the end, I have added a function to find the shortest path between start and end node,
avoiding all obstacles. I have also added a random test case.

'''


class Node:
    def __init__(self, position):
        self.position = position
        self.g_cost = 0  # cost from start node
        self.h_cost = 0  # heuristic cost (estimated cost to goal)
        self.parent = None

    @property
    def f_cost(self):
        return self.g_cost + self.h_cost

    def __lt__(self, other):    # for comparing nodes while using min heap.
        return self.f_cost < other.f_cost

class A_Star:
    def __init__(self, grid):
        self.grid = grid
        self.open_set = []
        self.closed_set = set()
    
    def push_to_open(self, node):  #To keep the open set sorted according to f_cost, in non-increasing order
        l=0
        r=len(self.open_set)-1
        while(l<=r):
            avg=int((l+r)/2)
            if node>self.open_set[avg]:
                r=avg-1
            else:
                l=avg+1
        self.open_set.insert(l, node)
    
    def pop_open(self):     #To remove and return the node with least f_cost.
        return self.open_set.pop()

    def get_neighbours(self, node):
        neighbours = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x, y = node.position[0] + dx, node.position[1] + dy
            if (0<=x and x<len(self.grid)) and (0<=y and y<len(self.grid[0])) and self.grid[x][y]!=1:
                neighbours.append(Node((x, y)))
        return neighbours

    def find_h_cost(self, a, b):
        return abs(a.position[0] - b.position[0]) + abs(a.position[1] - b.position[1])

    def final_path(self, end_node):
        path = []
        current_node = end_node
        while current_node is not None:  #As the start node's parent is None
            path.append(current_node.position)
            current_node = current_node.parent
        return path[::-1]

    def find_path(self, start, end):
        start_node = Node(start)
        end_node = Node(end)
        self.push_to_open(start_node)
        while self.open_set:
            current_node = self.pop_open()
            if current_node.position == end_node.position:
                return self.final_path(current_node)

            self.closed_set.add(current_node.position)
            for neighbour in self.get_neighbours(current_node):
                if neighbour.position in self.closed_set:
                    continue
                
                tentative_g_cost = current_node.g_cost + 1
                if neighbour not in self.open_set or tentative_g_cost < neighbour.g_cost:
                    neighbour.g_cost = tentative_g_cost
                    neighbour.h_cost = self.find_h_cost(neighbour, end_node)
                    neighbour.parent = current_node
                    if neighbour not in self.open_set:
                        self.push_to_open(neighbour)

        return None




def find_sol(grid, start, end):
    a_star = A_Star(grid)
    return a_star.find_path(start, end)



if __name__=="__main__":
    #In the grid, 1s represent obstacles and 0s represent usable places.
    test_grid = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0]
    ]
    
    start = (0, 2)
    end = (8, 15)

    a_star = A_Star(test_grid)
    path = a_star.find_path(start, end)
    if path:
        print("Path found:", path)
        print("__________________________________")
        for i in range(len(test_grid)):
            print("|", end="")
            for j in range(len(test_grid[0])):
                if (i,j)==start:
                    print('s ', end='')
                elif (i,j)==end:
                    print('e ', end='')
                elif (i,j) in path:
                    print('. ', end='')
                elif test_grid[i][j]==0:
                    print("  ", end='')
                else:
                    print("X ", end='')
            print("|")
        print("----------------------------------")
        
    else:
        print("No path found.")

