import numpy as np
import functools

def isBool(var):
    return type(var) == type(True)

def distance(monster_1,monster_2):
    # euclidean distance
    return np.linalg.norm(np.array(monster_1)-np.array(monster_2))

class MonsterClassificationAgent:
    def __init__(self):
        #If you want to do any initial processing, add it here.
        pass

    def transform_monster(self,monster):
        size = {"tiny":0, "small":1, "medium":2, "large":3, "huge":4}
        color = {"black":0, "white":1, "brown":2, "gray":3, "red":4, "yellow":5, "blue":6, "green":7, "orange":8, "purple":9}
        covering = {"fur":0, "feathers":1, "scales":2, "skin":3}
        foot_type = {"paw":0, "hoof":1, "talon":2, "foot":3, "none":4}

        m = []

        for key in monster:
            value = monster[key]

            if key == "size":
                m.append(size[value])
            elif key == "color":
                m.append(color[value])
            elif key == "covering":
                m.append(covering[value])
            elif key == "foot-type":
                m.append(foot_type[value])
            elif isBool(value):
                m.append(1 if value == True else 0)
            else:
                m.append(value)


        return m

    def solve(self, samples, new_monster):

        #Add your code here!
        #
        #The first parameter to this method will be a labeled list of samples in the form of
        #a list of 2-tuples. The first item in each 2-tuple will be a dictionary representing
        #the parameters of a particular monster. The second item in each 2-tuple will be a
        #boolean indicating whether this is an example of this species or not.
        #
        #The second parameter will be a dictionary representing a newly observed monster.
        #
        #Your function should return True or False as a guess as to whether or not this new
        #monster is an instance of the same species as that represented by the list.

        k = 3

        transformed = self.transform_monster(new_monster)
        distances = []

        for tup in samples:
            monster = tup[0]
            monster_class = tup[1]

            d = distance(self.transform_monster(monster),transformed)

            distances.append((monster,monster_class,d))

        def compare(x,y):
            return x[2] - y[2]
        
        distances = sorted(distances,key=functools.cmp_to_key(compare))

        true_count = 0
        false_count = 0

        for i in range(k):
            monster_class = distances[i][1]
            if monster_class == True:
                true_count += 1
            else:
                false_count += 1

        if true_count > false_count:
            return True
        else:
            return False