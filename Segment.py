from Point2D import Point2D
class Segment:
# Define a line between two 2DPoints.

    def __init__(self, start_p, end_p):
    # Receives 2 points and init an object and it's name.
        self.__start_p = start_p
        self.__end_p = end_p
        self.__name = "Line " + start_p.obj_id + " "+ end_p.obj_id

    ## getter method
    @property
    def start_p(self):
        return self.__start_p
    ## setter method
    @start_p.setter
    def start_p(self, new_value):
        if not isinstance(new_value, (int, float)):
            raise TypeError("Value must be a number")
        self.__start_p = new_value

    ## getter method
    @property
    def end_p(self):
        return self.__end_p
    ## setter method
    @end_p.setter
    def end_p(self, new_value):
        if not isinstance(new_value, (int, float)):
            raise TypeError("Value must be a number")
        self.__end_p = new_value

    @property
    def name(self):
        return self.__name
    ## setter method
    @name.setter
    def name(self, new_value):
        if not isinstance(new_value, str):
            raise TypeError("Value must be a string")
        self.__name = new_value

    def __str__(self):
        #printing setting
        res = '''{name}: Start point={start_p} ,End point={end_p}'''.format(name=(self.name),
                                                                  start_p=(
                                                                  (self.start_p.x, self.start_p.y)),
                                                                  end_p=((self.end_p.x, self.end_p.y)))
        return res

    def segment_length(self):
        #returns the distance of the segment
        return self.start_p.distance_to_point(self.end_p)