def test_solution(initial_sheep, initial_wolves,moves):

    left_sheep = initial_sheep
    left_wolves = initial_wolves
    right_sheep = 0
    right_wolves = 0

    boat_direction = 1
    for move in moves:

        # update state
        left_sheep -= move[0]*boat_direction
        left_wolves -= move[1]*boat_direction
        right_sheep += move[0]*boat_direction
        right_wolves += move[1]*boat_direction

        # check constraints

        # check if animal amounts are valid on either side
        # makes sure we don't take more than available animals from either side
        if (left_sheep < 0 or left_wolves < 0 or left_sheep > initial_sheep or left_wolves > initial_wolves
             or right_sheep < 0 or right_wolves < 0 or right_sheep > initial_sheep or right_wolves > initial_wolves
             ):
                raise Exception("Not enough animals")
        
        # check if the animals fit on the boat
        if not ((0 < move[0] + move[1] and move[0] + move[1] < 3) and move[0] >= 0 and move[1] >= 0):
             raise Exception("Can't fit this many animals on the boat")
        
         # make sure there aren't more wolves than sheep on either side
        if (left_sheep != 0 and left_sheep < left_wolves) or (
            right_sheep != 0 and right_sheep < right_wolves):
            raise Exception("The wolves ate the sheep")

        boat_direction = -boat_direction

    if right_sheep == initial_sheep and right_wolves == initial_wolves:
         print("(initial_sheep=",initial_sheep,",initial_wolves=",initial_wolves,") was correctly solved")
    elif len(moves) != 0:
         raise Exception("Not all animals crossed the river")
    else:
         print("(initial_sheep=",initial_sheep,",initial_wolves=",initial_wolves,") no solution was provided")
