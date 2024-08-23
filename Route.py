from Polyline import Polyline

class Route(Polyline): # Route class inherits from Polyline
    def __init__(self, points, id, s_polygon, t_polygon):
        """
        :param points: Route's assemble points
        :param id: Route's id, as formed during UI's "Load Routes" function
        :param s_polygon: route's starting polygon
        :param t_polygon: route's ending polygon
        """
        super().__init__(points)  # now, route has segments (=list) and name(=string)
        self.s_polygon = s_polygon
        self.t_polygon = t_polygon
        self.__id = id
        self.points = points #list of Point2D-points

    def route_length(self):
        """
           calculate route's length by the method distance_to_point() of Point2D class.
        :return: float-instance length of the route.
        """
        tot_distance = 0.0
        for i in range (len(self.points)-1):
            tot_distance=+ self.points[i].distance_to_point(self.points[i+1])
        return tot_distance

    ## getter method
    @property
    def id(self):
        return self.__id

    @property
    def coords(self):
        """
        Get the route coordinates as a list of tuples.

        Returns:
            List of tuples representing the route coordinates- [(y1, x1), (y2, x2), ...]
        """
        new_list = []
        for point in self.points:
            new_list.append((point.y, point.x))
        return new_list

    def __str__(self):
        #printing setting
        res = 'why'
        #res = '''Route_id: {D} S_polygon: {S} T_polygon: {T}'''.format(P=(self.__id), S=(self.s_polygon.id), T=(self.t_polygon.id))
        return res