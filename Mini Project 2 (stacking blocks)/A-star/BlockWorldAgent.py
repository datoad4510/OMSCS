from state import State
import heapq
import copy

class BlockWorldAgent:
    def __init__(self):
        #If you want to do any initial processing, add it here.
        pass
    
    def generate_next_states(self,state):
        next_states = []
        arrangement = state.blocks
        
		# for the top block of every stack
        for idx, block_stack in enumerate(arrangement):
            top_block = block_stack[-1]
            new_arrangement = copy.deepcopy(state.blocks)
            new_arrangement[idx].pop()
            
			# move it onto every other stack
            for other_idx,block_stack in enumerate(arrangement):
                if idx == other_idx:
                    continue
                
                blocks = copy.deepcopy(new_arrangement)
                blocks[other_idx].append(top_block)
                distance_from_start = state.distance_from_start + 1
                previous_move = (top_block,new_arrangement[other_idx][-1])
                blocks = list(filter(None,blocks))
                next_states.append(State(blocks,distance_from_start,previous_move,state))
            
			# move onto the table
            new_arrangement.append([top_block])
            distance_from_start = state.distance_from_start + 1
            previous_move = (top_block,"Table")
            blocks = new_arrangement
            blocks = list(filter(None,blocks))
            next_states.append(State(blocks,distance_from_start,previous_move,state))
        
        return next_states
    

    def solve(self, initial_arrangement, goal_arrangement): 
        #Add your code here! Your solve method should receive
		#as input two arrangements of blocks. The arrangements
		#will be given as lists of lists. The first item in each
		#list will be the bottom block on a stack, proceeding
		#upward. For example, this arrangement:
		#
		#[["A", "B", "C"], ["D", "E"]]
		#
		#...represents two stacks of blocks: one with B on top
		#of A and C on top of B, and one with E on top of D.
		#
		#Your goal is to return a list of moves that will convert
		#the initial arrangement into the goal arrangement.
		#Moves should be represented as 2-tuples where the first
		#item in the 2-tuple is what block to move, and the
		#second item is where to put it: either on top of another
		#block or on the table (represented by the string "Table").
		#
		#For example, these moves would represent moving block B
		#from the first stack to the second stack in the example
		#above:
		#
		#("C", "Table")
		#("B", "E")
		#("C", "A")

        State.target_state = goal_arrangement
        
        initial_state = State(initial_arrangement,0,-1,None)
        
        search_tree = set()
        
        priority_queue = []
        priority_queue.extend(self.generate_next_states(initial_state))
        heapq.heapify(priority_queue)
        # root of the tree, no parent
        search_tree.add(tuple(map(tuple, initial_arrangement)) )
        
        while len(priority_queue) != 0:
             smallest_heur = heapq.heappop(priority_queue)
             next_states = self.generate_next_states(smallest_heur)
             target_found = False
             for state in next_states:
                 blocks_tup = tuple(map(tuple, state.blocks)) 
                 if blocks_tup not in search_tree:
                     search_tree.add(blocks_tup)
                     heapq.heappush(priority_queue,state)
                     if sorted(state.blocks) == sorted(goal_arrangement):
                         target_found = True
                         break

             if target_found:
                 break
             

        path_stack = []

        # state with the smallest f will be the goal state
        running_state = heapq.heappop(priority_queue)
        
        while running_state.previous_move != -1:
            path_stack.append(running_state.previous_move)
            running_state = running_state.previous_state
        
        path_stack.reverse()

        return path_stack