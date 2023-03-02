# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

from PIL import Image
from PIL import ImageOps
import numpy as np
import os
import random

def image_eq(image1,image2):
    if image1.size != image2.size:
        return False

    arr1 = np.array(image1)
    arr2 = np.array(image2)

    intersection = 0
    for i in range(len(arr1)):
        for j in range(len(arr1[0])):
            if np.array_equal(arr1[i][j],arr2[i][j]):
                intersection += 1

    error = 1 - intersection / (image1.size[0] * image1.size[1])

    if error < 0.03:
        return True
    else:
        return False
    
def flip_vertical(image):
    return ImageOps.flip(image)

def flip_horizontal(image):
    return ImageOps.mirror(image)

def rot_all(image):
    deg = 45

    rotations = dict()

    while deg != 360:
        rotations[deg] = image.rotate(deg,fillcolor="white")
        deg += 45

    return rotations

def count_colors(image):
    arr = np.array(image)
    unique, counts = np.unique(arr, return_counts=True)
    freqs = dict(zip(unique, counts))
    black = freqs[0] / 3
    white = (freqs[255] - black) / 4

    return {"black":black,"white":white}

def dimensions(image):
    return image.size

def PIXEL_AND(pixel1,pixel2):
    black = np.array([0,0,0,255])
    white = np.array([255,255,255,255])
    if np.array_equal(pixel1,black) and np.array_equal(pixel2,black):
        return black
    else:
        return white
    
def PIXEL_OR(pixel1,pixel2):
    black = np.array([0,0,0,255])
    white = np.array([255,255,255,255])
    if np.array_equal(pixel1,black) or np.array_equal(pixel2,black):
        return black
    else:
        return white
    
def PIXEL_XOR(pixel1,pixel2):
    black = np.array([0,0,0,255])
    white = np.array([255,255,255,255])
    if not np.array_equal(pixel1,pixel2) and (np.array_equal(pixel1,black) or np.array_equal(pixel2,black)):
        return black
    else:
        return white

def logical_op(image1,image2,op):
    arr1 = np.array(image1)
    arr2 = np.array(image2)
    for i in range(len(arr1)):
        for j in range(len(arr1[0])):
            arr1[i,j] = op(arr1[i,j],arr2[i,j])

    return Image.fromarray(arr1)

def find_patterns_2x2(image_A,image_B,image_C):
    # consists of 3-tuples: ("A","B","flip_vertical"),("A","C","equal") etc.
    patterns = []

    rotations_A = rot_all(image_A)
    flip_vertical_A = flip_vertical(image_A)
    flip_horizontal_A = flip_horizontal(image_A)

    # looking for equality patterns
    if image_eq(image_A,image_B):
        patterns.append(("A","B","equal"))
    if image_eq(image_A,image_C):
        patterns.append(("A","C","equal"))


    # flip patterns
    if image_eq(flip_vertical_A,image_B):
        patterns.append(("A","B","flip_vertical"))
    if image_eq(flip_horizontal_A,image_B):
        patterns.append(("A","B","flip_horizontal"))
    if image_eq(flip_vertical_A,image_C):
        patterns.append(("A","C","flip_vertical"))
    if image_eq(flip_horizontal_A,image_C):
        patterns.append(("A","C","flip_horizontal"))


    # rotation patterns
    for deg, rot_img_A in rotations_A.items():
        if image_eq(rot_img_A,image_B):
            patterns.append(("A","B","rot_{}".format(deg)))


    for deg, rot_img_A in rotations_A.items():
        if image_eq(rot_img_A,image_C):
            patterns.append(("A","C","rot_{}".format(deg)))

    return patterns


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self,problem):


        if problem.problemType != "2x2":
            return random.randint(1,8)
        # if problem.name != "Basic Problem B-01":
        #     return -1
        
        # my_path = os.path.abspath(os.path.dirname(__file__))
        # path1 = os.path.join(my_path,"Problems","Basic Problems B","Basic Problem B-01","A.png")
        # path2 = os.path.join(my_path,"Problems","Basic Problems B","Basic Problem B-01","B.png")
        # path3 = os.path.join(my_path,"Problems","Basic Problems B","Basic Problem B-01","1.png")
        # path4 = os.path.join(my_path,"Problems","Basic Problems E","Basic Problem E-03","1.png")

        # with Image.open(path1) as img1, Image.open(path2) as img2, Image.open(path3) as img3, Image.open(path4) as img4:
        #     img1.show()
        #     img4.show()

        #     logical_op(img1,img4,PIXEL_AND).show()
        #     logical_op(img1,img4,PIXEL_OR).show()
        #     logical_op(img1,img4,PIXEL_XOR).show()

        
        # print(problem.name,problem.problemType,problem.problemSetName,problem.hasVisual,problem.hasVerbal)

        answer_images = []

        image_A = None
        image_B = None
        image_C = None

        # initialize
        for label, image in problem.figures.items():
            path = image.visualFilename
            img = Image.open(path)
            if label == "A":
                image_A = img
            elif label == "B":
                image_B = img
            elif label == "C":
                image_C = img
            else:
                answer_images.append((img,label))

        patterns = find_patterns_2x2(image_A,image_B,image_C)

        if len(patterns) == 0:
            return random.randint(1,6)
        else:
            for pattern in patterns:
                img_to_check = None
                if pattern[1] == "B":
                    img_to_check = image_C
                elif pattern[1] == "C":
                    img_to_check = image_B
    
                for answer_img, label in answer_images:
                    # check for pattern

                    func = pattern[2]
                    if func == "equal":
                        if image_eq(img_to_check,answer_img):
                            return int(label)
                    elif func == "flip_horizontal":
                        if image_eq(flip_horizontal(img_to_check),answer_img):
                            return int(label)
                    elif func == "flip_vertical":
                        if image_eq(flip_vertical(img_to_check),answer_img):
                            return int(label)
                    else:
                        spl = func.split("_")
                        deg = int(spl[1])
                        rotated_img = img_to_check.rotate(deg,fillcolor="white")
                        if image_eq(rotated_img,answer_img):
                            return int(label)


        # free memory
        image_A.close()
        image_B.close()
        image_C.close()
        for img, label in answer_images:
            img.close()
           

        return random.randint(1,6)