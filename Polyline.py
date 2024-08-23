from Point2D import Point2D
from Segment import Segment

class Polyline:
# Polyline class is a collection of continuous segments

    def __init__(self, points, name=""):
    # receives list of points and defines a polyline object, base on the segments between every two consective points
        self.__segments = list(map(lambda x, y: Segment(x,y), points, points[1:]))
        temp_string = "Polyline "
        for i in points:
            temp_string = temp_string + i.obj_id
        self.__name = temp_string

## getter method
    @property
    def segments(self):
        return self.__segments
    ## setter method
    # none

    ## getter method
    @property
    def name(self):
        return self.__name
    ## setter method
    @name.setter
    def name(self, new_value):
        if not isinstance(new_value, str):
            raise TypeError("Value must be a string")
        self.__name = new_value

    def __getitem__(self, item):
    ## allow access to every cell in the 'segments' list by use [] on Polyline objects.
        return self.segments[item]

    def poly_length(self):
    ## returns the polyline's total length.
        total_len = 0
        for i in self:
            total_len +=  i.segment_length()
        return total_len

    def __str__(self):
        #printing setting
        res = ""
        for i in range(len(self.segments)):
            res = res + '''{Poly_name}: {Seg_name}: Start point={sp}: X={x1}, Y={y1}, End point={ep}:  X={x2}, Y={y2} \n'''.format(Poly_name=self.name,
                                                                                        Seg_name=self[i].name,
                                                                                        sp=self[i].start_p.obj_id,
                                                                                        x1=self[i].start_p.x,
                                                                                        y1=self[i].start_p.y,
                                                                                        ep=self[i].end_p.obj_id,
                                                                                        x2=self[i].end_p.x,
                                                                                        y2=self[i].end_p.y
                                                                                         )
        return res