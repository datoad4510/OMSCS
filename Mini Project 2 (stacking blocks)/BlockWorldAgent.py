import copy

class BlockWorldAgent:
    running_arrangement = []

    def __init__(self):
        #If you want to do any initial processing, add it here.
        pass

    def free_top(self,arrangement, block):
        # remove blocks that are on top of the given block
        moves = []
        for stack in arrangement:
            found_stack = False
            for running_block in stack:
                if running_block == block:
                    found_stack = True
                    break

            if found_stack:
                while stack[-1] != block:
                    top_block = stack[-1]
                    stack.pop()

                    # move the top block off of the stack and onto the table
                    arrangement.append([top_block])
                    moves.append((top_block,"Table"))
                
                break
        

        return moves


    def convert_arrangement_to_relations(self,arrangement):
        relations = dict()
        for stack in arrangement:
            for idx,block in enumerate(stack):
                if idx == 0:
                    relations[block] = "Table"
                else:
                    previous_block = stack[idx-1]
                    relations[block] = previous_block
        
        return relations

    def find_subproblems(self,arrangement,goal_arrangement):
        # finds next subproblems to solve
        relations = self.convert_arrangement_to_relations(arrangement)

        # print(arrangement,goal_arrangement)
        # print(relations)
        
        subproblems = []

        for stack in goal_arrangement:
            last_correct_block_idx = -1


            for idx, block in enumerate(stack):
                if idx != 0 and relations[block] == stack[idx-1]:
                    last_correct_block_idx += 1
                elif idx == 0 and relations[block] == "Table":
                    last_correct_block_idx += 1
                else:
                    break

            if last_correct_block_idx == -1:
                subproblems.append((stack[last_correct_block_idx+1],"Table"))
            elif last_correct_block_idx != len(stack) - 1:
                subproblems.append((stack[last_correct_block_idx+1],stack[last_correct_block_idx]))

        # find already correct substacks
        return subproblems

    def move(self,arrangement, move_tup):
        
        moves = []
        
        # ? process moving onto the table separately
        # todo: make the code dry!
        if move_tup[1] == "Table":
            moves.extend(self.free_top(arrangement,move_tup[0]))
            moves.append(move_tup)

            for stack in arrangement:
                if stack[-1] == move_tup[0]:
                    stack.pop()

            arrangement.append([move_tup[0]])

            # remove empty stacks
            for stack in arrangement:
                # get rid of empty stack
                if len(stack) == 0:
                        arrangement.remove([])
                
            return moves


        # move block1 on top of block2
        moves1 = self.free_top(arrangement,move_tup[0])
        moves2 = self.free_top(arrangement,move_tup[1])

        # and now move block1 onto block2

        for stack in arrangement:
            if stack[-1] == move_tup[0]:
                stack.pop()

            elif stack[-1] == move_tup[1]:
                stack.append(move_tup[0])

        # remove empty stacks
        for stack in arrangement:
            # get rid of empty stack
            if len(stack) == 0:
                    arrangement.remove([])

        moves.extend(moves1)
        moves.extend(moves2)
        moves.append(move_tup)

        return moves

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

        self.running_arrangement = copy.deepcopy(initial_arrangement)

        moves = []

        while sorted(self.running_arrangement) != sorted(goal_arrangement):
            subproblems = self.find_subproblems(self.running_arrangement,goal_arrangement)
            for subproblem in subproblems:
                intermediate_moves = self.move(self.running_arrangement,subproblem)
                moves.extend(intermediate_moves)

        return moves