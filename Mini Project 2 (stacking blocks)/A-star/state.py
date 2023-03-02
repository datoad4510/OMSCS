class State:
  target_state = []

  def state_delta(self):
     # convert both current state and target state to sets of 2-tuples
     # where the tuple ("A","B") means A is on top of B.
     # reutrn the length of their set intersection
     current_state_set = set()
     target_state_set = set()

     for block_stack in self.blocks:
        current_state_set.update(list(zip(block_stack,block_stack[1::])))
        current_state_set.add((block_stack[-1],"Table"))

     for block_stack in self.target_state:
        target_state_set.update(list(zip(block_stack,block_stack[1::])))
        target_state_set.add((block_stack[-1],"Table"))

     return len(current_state_set.symmetric_difference(target_state_set))

  def __init__(self, blocks, distance_from_start, previous_move, previous_state):
      self.blocks = blocks
      self.distance_from_start = distance_from_start
      self.previous_move = previous_move
      self.previous_state = previous_state
  
  # custom "less than" operator for our heap
  def __lt__(self, other):
      
      # since state_delta is always less than the actual distance from
      # the current state to the target state, A* will return the optimal answer
      # f(n) = g(n) + h(n). g(n) == start_dist, h(n) == state_delta() <= h*(n) == actual distance

      # min heap
      # return (self.distance_from_start + self.state_delta()) < (other.distance_from_start + other.state_delta())
      return (self.distance_from_start + self.state_delta()) < (other.distance_from_start + other.state_delta())