import numpy as np
import string
from abc import ABC, abstractclassmethod  ### in order to prevent 'none' as we taught in lecture 2
import math

class Point2D(ABC):
# 2D point in cartesian coordinates
    count = 0  # Class variable to keep track of the point names
# Define a single object
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        Point2D.count += 1
        self.__obj_id = "point" + str(Point2D.count) # Assign the current character

    ## getter method
    @property
    def x(self):
        return self.__x

    ## setter method
    @x.setter
    def x(self, new_value):
        if not isinstance(new_value, (int, float)):
            raise TypeError("Value must be a number")
        self.__x = new_value

    ## getter method
    @property
    def y(self):
        return self.__y

    ## setter method
    @y.setter
    def y(self, new_value):
        if not isinstance(new_value, (int, float)):
            raise TypeError("Value must be a number")
        self.__y = new_value

    ## getter method
    @property
    def obj_id(self):
        return self.__obj_id

    ## setter method
    @obj_id.setter
    def obj_id(self, new_value):
        if not isinstance(new_value, str):
            raise TypeError("Value must be a string")
        self.__obj_id = new_value

    ## new method
    def distance_to_point(self, point):
        # receive a point and return the distance between it and the current point
        return np.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)

    ## Distance static method
    def static_distance_to_point(point_1, point_2):
        # receives two points and return the distance between them
        return np.sqrt(((point_1.x - point_2.x) ** 2 + (point_1.y - point_2.y) ** 2))

    ## new method:
    def point_translate(self, dx, dy):
        # receives shifting values for x and y and moves the current point respectively. by matrix multiplication.
        vector = np.array([
        [self.x],
        [self.y],
        [1]])
        tras_mat = np.array([
            [1, 0, dx],
            [0, 1, dy],
            [0, 0, 1]
        ])
        product = tras_mat @ vector ## matrix multiplication
        for i in range(len(product)): ## vector normalizing
            product[i] = product[i] / float(vector[2])
        self.x = float(product[0])
        self.y = float(product[1])

    ## new method:
    def rotation_point(self, angle):
        # receives angle (°) and moves the current point respectively. by matrix multiplication.
        r_vec = np.array([
        [self.x],
        [self.y],
        [1]])
        cos_theta = np.cos((angle)*math.pi/180)
        sin_theta = np.sin((angle)*math.pi/180)
        rotation_matrix = np.array([
            [cos_theta, -sin_theta, 0],
            [sin_theta, cos_theta, 0],
            [0, 0, 1]
        ])
        product = rotation_matrix @ r_vec
        for i in range(len(product)): ## vector normalizing
            product[i] = product[i] / float(r_vec[2])
        self.x = float(product[0])
        self.y = float(product[1])

    def __str__(self):
        #printing setting
        res = '''Point_id: {P} Point coordinates: {C}'''.format(P=(self.obj_id),
                                          C=(self.x, self.y))
        return res