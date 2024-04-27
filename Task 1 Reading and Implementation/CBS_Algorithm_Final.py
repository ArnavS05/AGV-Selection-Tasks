'''
EXPLANATION OF MY CODE:
I will be using the second method shown in Fig.3 of the given research paper (Sharon et. al., 2015).
Thus, each conflict will have only first two conflicting agents. As mentioned in the research paper
(just after Fig. 3), this would be equivalent to taking all conflicting agents at once.

The conditions of my multi-agent path finder are:
1. There can be k agents (where k>=2).
2. No agent can come at a halt unless it reaches its goal.
3. Not more than one agent can be at a particular position at a given time.
4. Not more than one agent can cross a particular edge between time t and t+1.
5. This code outputs the most efficient set of paths for the agents where efficiency
   is based on cost of the solution, which is sum of number of steps taken by each agent.


Time starts with 0 and increments by 1 at each step.

The grid is zero indexed and the top-left cell represents the position (0,0).
If a position is (x,y), then x would represent the row and y would be the column.

A_Star_Path_Finding_Algorithm (imported in this code) is the first part of Task 1 done by me.


CLASS DESCRIPTIONS:
Class Agent:
Used to create an agent with its start and end.

Class Conflict:
Used to create a conflict (edge or vertex conflict).
conflict_type can be "edge" or "vertex".
position2 is None in case of vertex conflicts.
In case of edge conflicts, position1 is the position of agent1 at time='time'
and also the position of agent2 at time='time'+1. On the other hand, position2
is the position of agent1 at time='time'+1 and also the position of agent2 at time='time'.

Class Constraint:
Used to create a constraint where 'agent' cannot be at 'position' at time='time.

Class Leaf:
It represents a node of the Constraint Tree of the CBS algorithm.
It stores the parent (which is None for root leaf), children, constraints and proposed solution of itself.
It has a function to find conflicts in its own solution and a property to find the cost of its solution.

Class Constraint_Tree:
It is the main part of the CBS algorithm.
It has a list (named open) which stores leaves (or nodes) sorted according to the cost of their solutions.
To keep the list sorted, this class has a function called push_to_open to add a new leaf to the list. The function 
uses binary search and thus its time complexity is O(logn).
To pop the leaf with least cost from the list named open, a function named pop_open has been implemented. 
It has a function to update a leaf's solution according to new constraints. I have described the function 
a few lines later. Finally, this class also has the 'find_result' function which implements the CBS algorithm 
given in the research paper, Sharon et. al., 2015.


If a conflict is of type 'vertex', then the parent leaf would be branched down to two children leaves as described 
in the research paper, Sharon et. al., 2015. On the other hand, when the conflict is of type 'edge', then, the 
parent leaf would be branched down to two children leaves where the leaves would have the new constraints as 
Constraint(agent_i, position2, 'time'+1) and Constraint(agent_j, position1, 'time'+1) (refer to description of 
classes above) respectively.

Idea behind the function 'update_leaf_solution' of the class Constraint_Tree:
Let the previous path of agent_i be [p_0, p_1, p_2, ..., p_k, ..., p_n] where agent_i is the constraint agent 
and p_k is the constraint position (and k is the constraint time).
Then, this function iterates 'pos' from p_k-1 to p_1 and in each iteration, the function finds the neighbouring 
position of 'pos' which are neither obstacles, and nor the position which come after 'pos' in the previous path. 
The function maintains a list of all possible solutions which are 0->pos->neighbour->goal for each 'pos' and 
each of its possible neighbours. Here, 0->pos is directly taken from previous path and neighbout->goal is found 
using the A* algorithm. Finally, the path which satisfies all constrints (related to agent_i) of the leaf and has 
least number of steps is made to be the updated path of agent_i.


At the end, I have made a function (named 'test'), which takes two arguments, the first one being a grid of any 
size and the second one being a list of instances of class Agent, where the list can have ANY NUMBER OF AGENTS. 
This function can be used to test my code. The function gives the solutions neatly, in two forms, as a list of 
steps for all agents and also a diagram showing paths of all agents. But, the diagramatic representation may not
be the best way to see the result as it won't show whether the robot is passing through a given position once or
more than once. For that, the list of steps must be seen. Diagramatic form is just an aid.
Below the function, I have made some random test cases which can be run.
Feel free to test the code with more test cases.

'''



import A_Star_Path_Finding_Algorithm as A_st

class Agent:
    def __init__(self, start, end):
        self.start=start
        self.end=end


class Conflict:
    def __init__(self, conflict_type, agent1, agent2, time, position1, position2=None):
        self.agent1=agent1
        self.agent2=agent2
        self.conflict_type=conflict_type      #"edge" or "vertex"
        self.position=position1
        self.position2=position2    #used in case of edge conflict
        self.time=time


class Constraint:
    def __init__(self, agent, position, time):
        self.agent=agent
        self.position=position
        self.time=time


class Leaf:    #A node in the Constraint Tree
    def __init__(self, constraints, parent, agents):
        self.agents=agents
        self.constraints=constraints if constraints else []
        self.parent=parent
        self.children=[]
        self.solution=None
     
    def find_conflict(self):
        #Finding vertex conflict (only the first two conflicting agents)
        for i in range(len(self.solution)-1):
            for j in range(i+1, len(self.solution)):
                for k in range(len(self.solution[i])):
                    try:
                        if self.solution[i][k]==self.solution[j][k]:
                            return Conflict("vertex", self.agents[i], self.agents[j], k, self.solution[i][k])
                    except:
                        continue

        #Finding edge conflict (only the first two conflicting agents)
        for i in range(len(self.solution)-1):
            for j in range(i+1, len(self.solution)):
                for k in range(len(self.solution[i])-1):
                    try:
                        if (self.solution[i][k]==self.solution[j][k+1] and self.solution[i][k+1]==self.solution[j][k]):
                            return Conflict("edge", self.agents[i], self.agents[j], k, self.solution[i][k], self.solution[i][k+1])
                            
                    except:
                        continue

        return None       #return None if no conflict found

    @property
    def f_cost(self):   #Taking the cost function as the sum of number of steps taken by each agent
        sum1=0
        for i in self.solution:
            sum1+=len(i)
        return sum1

    def __lt__(self, other_leaf):
        #According to Sharon et. al., 2015, tie has to be broken based on number of constraints.
        if self.f_cost!=other_leaf.f_cost:
            return self.f_cost < other_leaf.f_cost
        else:           #If f_cost is same, the leaf with less constraints is preferred
            return len(self.constraints)<len(other_leaf.constraints)


class Constraint_Tree:
    def __init__(self):
        self.root=Leaf(None, None, None)
        self.agents=[]
        self.open=[]

    def push_to_open(self, leaf):  #To keep the open set sorted according to f_cost, in non-increasing order.
        l=0
        r=len(self.open)-1
        while(l<=r):
            avg=int((l+r)/2)
            if leaf>self.open[avg]:
                r=avg-1
            else:
                l=avg+1
        self.open.insert(l, leaf)
    
    def pop_open(self):     #To remove and return the node with least f_cost.
        return self.open.pop()

    def update_leaf_solution(self, leaf):
        if leaf.solution is None:   #i.e. this leaf is the root leaf
            leaf.solution=[]
            for agent in self.agents:
                path=A_st.find_sol(self.grid, agent.start, agent.end)
                if path is None:
                    leaf.solution=None
                    return None
                else:
                    leaf.solution.append(path)
        else:
            new_constraint=leaf.constraints[-1]
            con_agent=new_constraint.agent
            con_agent_num=self.agents.index(con_agent)
            old_con_agent_path=leaf.solution[con_agent_num]
            possible_new_paths=[]   #Possible paths for con_agent
            con_time=new_constraint.time
            for pos in old_con_agent_path[con_time-1::-1]:
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    x, y = pos[0] + dx, pos[1] + dy
                    if (0<=x and x<len(self.grid)) and (0<=y and y<len(self.grid[0])) and self.grid[x][y]!=1 and ((x,y)!= old_con_agent_path[old_con_agent_path.index(pos)+1]):
                        path_part=A_st.find_sol(self.grid, (x,y), con_agent.end)
                        if path_part is not None:
                            new_path=old_con_agent_path[0:old_con_agent_path.index(pos)+1]+path_part
                            flag=True
                            for const in leaf.constraints:
                                if not (const.agent==con_agent and new_path[const.time]!=const.position):
                                    flag=False
                                    break
                            if flag==True:
                                possible_new_paths.append(new_path)
                                
            if possible_new_paths!=[]:
                #Now, returning the new path from possible_new_paths such that the path is shortest possible
                min_len=min([len(path) for path in possible_new_paths])
                for i in possible_new_paths:
                    if len(i)==min_len:
                        leaf.solution[con_agent_num]=i
                        break
            else:
                leaf.solution=None

    def find_result(self, grid, *agents):
        self.agents=agents
        self.grid=grid
        self.root.agents=agents
        self.update_leaf_solution(self.root)
        if self.root.solution is None:
            return None
        self.push_to_open(self.root)
        while self.open!=[]:
            current_leaf=self.pop_open()
            conflict=current_leaf.find_conflict()
            if conflict is None:
                return current_leaf.solution
            
            if conflict.conflict_type=="vertex":
                for agent in (conflict.agent1, conflict.agent2):
                    child=Leaf(current_leaf.constraints+[Constraint(agent, conflict.position, conflict.time)], current_leaf, agents)
                    current_leaf.children.append(child)
                    child.solution=current_leaf.solution
                    self.update_leaf_solution(child)
                    if child.solution is not None:
                        self.push_to_open(child)

            elif conflict.conflict_type=="edge":
                child=Leaf(current_leaf.constraints+[Constraint(conflict.agent1, conflict.position2, conflict.time+1)], current_leaf, agents)
                current_leaf.children.append(child)
                child.solution=current_leaf.solution
                self.update_leaf_solution(child)
                if child.solution is not None:
                    self.push_to_open(child)

                child=Leaf(current_leaf.constraints+[Constraint(conflict.agent2, conflict.position, conflict.time+1)], current_leaf, agents)
                current_leaf.children.append(child)
                child.solution=current_leaf.solution
                self.update_leaf_solution(child)
                if child.solution is not None:
                    self.push_to_open(child)

        return None
                
            


#Function to test my code:
def test(test_grid, agents):
    CT=Constraint_Tree()
    res=CT.find_result(test_grid, *agents)
    print("SAMPLE TEST")
    print("Grid: (1 represents obstacle)")
    print("_"*(len(test_grid[0])*2+2))
    for i in test_grid:
        print("|", end="")
        for j in i:
            print(j, end=" ")
        print("|")
    print("-"*(len(test_grid[0])*2+2))
    print()
    print("Agents:")
    for i in range(len(agents)):
        print(i+1, ". ", agents[i].start, " -> ", agents[i].end, sep="")
    print()
    
    if res is not None:
        print("Solution:")
        print("'X' represents obstacles. '.' represents path.")
        print("'s' represents start. 'g' represents goal.")
        for i in range(len(agents)):
            print("Path of agent ", i+1, ": ", res[i], sep="")
            if len(set(res[i]))!=len(res[i]):
                print('''While seeing the below diagramatic path, one should realise that
the agent is passing through one (or more) point(s) more than once.
Thus, one should also refer to the above list (showing the path) as well.''')
            print("_"*(len(test_grid[0])*2+2))
            for j in range(len(test_grid)):
                print("|", end="")
                for k in range(len(test_grid[0])):
                    if (j,k) == res[i][0]:
                        print("s ", end="")
                    elif (j,k) == res[i][-1]:
                        print("g ", end="")
                    elif (j,k) in res[i]:
                        print(". ", end="")
                    elif test_grid[j][k]==1:
                        print("X ", end="")
                    else:
                        print("  ", end="")
                print("|")
            print("-"*(len(test_grid[0])*2+2))
            print()
    else:
        print("No solution found")
    print()
    print("-"*80)
    print()



#Some sample test functions:

test([
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
    [Agent((0,0), (9,9)),
    Agent((0,9), (9,0)),
    Agent((0,5), (9,4)),
    Agent((3,8), (7,4)),
    Agent((6,2), (8,8)),
    Agent((9,3), (1,9))]
     )

test([
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
    [Agent((0,0), (9,9)),
    Agent((0,8), (9,0))]
     )

test([
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 1, 1, 1, 1, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [1, 1, 0, 1, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    ],
    [Agent((0,0), (9,9)),
    Agent((0,9), (9,0)),
    Agent((0,4), (9,5))]
     )

test([
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 1, 0, 0, 1, 1, 0],
        [0, 1, 0, 1, 0, 0, 0, 0],
        [1, 0, 0, 1, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 1, 0, 0, 0, 1]
    ],
    [Agent((0,0), (6,6)),
    Agent((0,5), (5,0))]
     )

test([
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1]
    ],
    [Agent((1,0), (1,6)),
    Agent((1,7), (1,0))]
     )

test([
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0]
    ],
     [Agent((0,0), (5,0)),
    Agent((1,0), (1,4)),
    Agent((0,1), (4,1))]
     )


