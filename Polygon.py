from Point2D import Point2D
class Polygon:
    counter = 0 # Class variable to keep track of the polygon's id
    def __init__(self, points, id=None):
        """
        :param points: boundary polygon's points
        :param id: polygon's id, as formed during UI's "Load Polygons" function
        """
        self.points = points #list of Point2D-points
        self.id = Polygon.counter
        Polygon.counter += 1
        
    @property
    def coords(self):
        """
        Get the polygon coordinates as a list of tuples.

        Returns:
            List of tuples representing the polygon coordinates- [(y1, x1), (y2, x2), ...]
        """
        new_list = []
        for point in self.points:
            new_list.append((point.y, point.x))
        # 24/11/23: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        print("the coords: ", new_list)
        return new_list
        
    def isInside(self, point):
        """
        Check if a given point is inside the polygon.

        Args:
            point (Point2D): The point to check.

        Returns:
            bool: True if the point is inside the polygon, False otherwise.
        """
        num_points = len(self.points)
        inside = False
        
        for i in range(num_points):
            current_point = self.points[i]
            next_point = self.points[(i + 1) % num_points]
            
            if (
                (point.y > min(current_point.y, next_point.y)) and
                (point.y <= max(current_point.y, next_point.y)) and
                (point.x <= max(current_point.x, next_point.x)) and
                (current_point.y != next_point.y)
            ):
                x_intersect = (
                    (point.y - current_point.y) * (next_point.x - current_point.x) / 
                    (next_point.y - current_point.y) + current_point.x
                )
                
                if current_point.x == next_point.x or point.x <= x_intersect:
                    inside = not inside
        return inside

#24/11/23: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# p1 = Point2D(1,0)
# p2 = Point2D(2,0)
# p3 = Point2D(1,1)
# p4 = Point2D(2,1)
# plist=[p1,p2,p3,p4]
# #        coo_list = list(map(lambda p: (p.y,p.x), plist)) # (x,y) equals (E,N)
# pol1 = Polygon(plist)
# temp_list= pol1.coords
