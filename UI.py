import tkinter as tk
import tkinter.filedialog as filedialog
from cgitb import text
from tkinter import messagebox
import tkintermapview
from Route import Route
from Point2D import Point2D
from Polygon import Polygon
import mimetypes
import os
from Graph import Graph

class UI(tk.Tk):
    def __init__(self):
        super().__init__()
    
        self.geometry(f"{800}x{600}")
        self.title("shortest path.py")
        
        toolbar_frame = tk.Frame(self, width=800, height=50, bg="gray")
        toolbar_frame.pack(side=tk.TOP, fill=tk.X)

        # create buttons on the toolbar frame:
        load_polygons_button = tk.Button(toolbar_frame, text="Load Polygons", command=self.load_polygons)
        load_polygons_button.pack(side=tk.LEFT)
        
        load_routes_button = tk.Button(toolbar_frame, text="Load Routes", command=self.load_routes)
        load_routes_button.pack(side=tk.LEFT)                        

        select_origin_button = tk.Button(toolbar_frame, text="Select Origin", command=self.select_origin)
        select_origin_button.pack(side=tk.LEFT)
        self.select_origin_flag = False # turns up when select origin button is clicked

        select_destination_button = tk.Button(toolbar_frame, text="Select Destination", command=self.select_destination)
        select_destination_button.pack(side=tk.LEFT)
        self.select_destination_flag = False # turns up when select destination button is clicked

        find_shortest_path_button = tk.Button(toolbar_frame, text="Find Shortest Path", command=self.find_shortest_path)
        find_shortest_path_button.pack(side=tk.LEFT)

        clear_route_button = tk.Button(toolbar_frame, text="Clear Route", command=self.clear_route)
        clear_route_button.pack(side=tk.LEFT)

        close_program_button = tk.Button(toolbar_frame, text="Close Program", command=self.close_program)
        close_program_button.pack(side=tk.LEFT)

        # create map widget
        self.map_widget = self.init_map()

        # create polygons list, and routes list
        self.polygons = []
        self.routes = []

        # create origin and destination polygon
        self.origin_p = None
        self.destination_p = None

    def init_map(self):
        try:
            # create map widget
            map_widget = tkintermapview.TkinterMapView(self, width=800, height=600, corner_radius=0)
            map_widget.pack(side=tk.BOTTOM)
            
            # set current widget position and zoom
            map_widget.set_position(32.777653,35.023630)  # technion, Israel
            map_widget.set_zoom(16)
            
            map_widget.add_left_click_map_command(self.left_click_event)

            return map_widget
        except Exception as e:
            print(f"Error: {e}")
    
    def left_click_event(self, coordinates_tuple):
        """
        define cases (and the following actions) follow user's left-click event
        :param coordinates_tuple: holds the user's on-map-click's coordinates (y,x).
        """
        self.left_click_event = coordinates_tuple #(y1,x1)

        # if select-origin-button is on:
        if (self.select_origin_flag):
            if(self.origin_p is None):
                self.origin_p = self.o_d_polygon_found(coordinates_tuple, "Origin") #stores the selected origin polygon using o_d_polygon_found method
            else:
                msg = messagebox.showinfo("attention", "Origin is already selected")
            self.select_origin_flag = False
        # if select-destination-button is on:
        if (self.select_destination_flag):
            if(self.destination_p is None):
                self.destination_p = self.o_d_polygon_found(coordinates_tuple, "Destination") #stores the selected destination polygon using o_d_polygon_found method
            else:
                msg = messagebox.showinfo("attention", "Destination is already selected")
            self.select_destination_flag = False

    def o_d_polygon_found(self, coordinates_tuple, o_d_string):
        """
        origin / destination polygon-finding method
        :param coordinates_tuple, and string symbolizes if origin or destination button is selected
        :return: a Polygon instance: the selected polygon (origin or destination, follow button's purpose), if found.
        """
        my_point = Point2D(coordinates_tuple[1], coordinates_tuple[0]) # create a Point2D instance using the coordinates
        for p in self.polygons:
            if (p.isInside(my_point)):
                self.map_widget.set_polygon(p.coords, outline_color='cyan', fill_color='green')
                return p  # return the polygon, only if the user left-clicks on one of the polygons.
        msg = messagebox.showinfo("error", "Couldn't find a polygon. Click on select "+ o_d_string+" again")
        return None

    def load_routes(self):
        """
        Loads a text file (only), separates written routes from it, and stored each in a list.
        Display the routes on the map, at the end.
        """
        file_path = self.browse_file()
        # get the MIME type of the file
        mime_type, _ = mimetypes.guess_type(file_path)
        # check if file's type is text
        if not (mime_type == "text/plain"):
            raise TypeError("File's type must be text")

        with open(file_path, "r", encoding='utf-8') as file:
            file_contents = file.read()
        # split_contents is a list, and each cell represent a route
        split_contents = file_contents.split('#')
        # with for loop we will insert to self.routes-list all routes from file
        # remember the 1st cell is empty, because '#' is the first char in the text file
        for q in range(1, len(split_contents)):
            route_cont = split_contents[q].split('\n') # holds every route content from file's split contents
            route_id = q # to track route's id
            # define: matrix is a list, its cells contain lists: the first list contains nothing,
            # and each of the rest contains a single coordinate.
            matrix = [row.split(",") for row in route_cont]

            route_i_points = [] # will contain points of a single route: each cell will contain one point
            for i in range(1, len(matrix)-1): # first row and last row are always empty
                route_i_points.append(Point2D(float(matrix[i][1]), float(matrix[i][0])))  # (x,y) equals (E,N)
            # defines start and end polygon to route
            for poly in self.polygons:
                if (poly.isInside(route_i_points[0])):
                    start_poly = poly
                    #24/11 #print("start poly: "+start_poly.coords)
                if (poly.isInside(route_i_points[-1])):
                    end_poly = poly
                    #24/11 #print("end poly: "+end_poly.coords)
            # create new route
            self.routes.append(Route(route_i_points, route_id, start_poly, end_poly)) # routes-list contains all routes
        file.close()
        self.show_routes()
        #24/11:#print("routes:"+self.routes[0])
            
    def load_polygons(self):
        """
        Loads a text file (only), separates written polygons from it, and stored each in a list.
        Display the polygons on the map, at the end.
        """
        file_path = self.browse_file()
        # get the MIME type of the file
        mime_type, _ = mimetypes.guess_type(file_path)
        # check if file's type is text
        if not (mime_type == "text/plain"):
            raise TypeError("File's type must be text")

        with open(file_path, "r", encoding='utf-8') as file:
            file_contents = file.read()
        # split_contents is a list, and each cell represent a polygon
        split_contents = file_contents.split('#')
        # with for loop we will insert to self.polygons-list all polygons from file
        # remember the 1st cell is empty, because '#' is the first char in the text file
        for q in range(1, len(split_contents)):
            poly_cont = split_contents[q].split('\n') # holds every polygon content from file's split contents
            poly_i_name = poly_cont[0]
            # define: matrix is a list, its cells contain lists: the first list contains the polygon's name,
            # and each of the rest contains a single coordinate.
            matrix = [row.split(",") for row in poly_cont]
            poly_i_points = [] # will contain points of a single polygon
            for i in range(1, len(matrix)-1): # first row is polygon's name, last row is always empty
                poly_i_points.append(Point2D(float(matrix[i][1]), float(matrix[i][0])))  # (x,y) equals (E,N)
            self.polygons.append(Polygon(poly_i_points, poly_i_name)) # polygons-list contains all polygons
        file.close()
        self.show_polygons()

    # load polygon method call for show polygon to display all polygon on map
    def show_polygons(self):
        self.map_widget.delete_all_polygon() #clear previously shown polygons
        for poly in self.polygons:
            self.map_widget.set_polygon(poly.coords, outline_color = 'red', fill_color= 'yellow')

    # load routes method call for show routes to display all routes on map
    def show_routes(self):
        self.map_widget.delete_all_path() #clear previously shown routes
        for route in self.routes:
            self.map_widget.set_path(route.coords, color = 'black', width=3)

    def browse_file(self):
    # Return: the user's selected file's path
        file_path = filedialog.askopenfilename(filetypes=[("txt Files", "*.txt")])
        return file_path

    # when click on select origin button, will hint to left_click_event method that the button is pushed.
    def select_origin(self):
        self.select_origin_flag = True

    # when click on select destination button, will hint to left_click_event method that the button is pushed.
    def select_destination(self):
        self.select_destination_flag = True

    # when click on find-shortest-path button:
    def find_shortest_path(self):
    #calculate and display the shortest path following the user's origin and destination select.
    # the caculation is done by the method shortestPath of a Graph instance, which is formed during find_shortest_path method.
        if (self.origin_p is not None and self.destination_p is not None):
            my_graph = Graph(self.routes, self.polygons)
            distance, shortest_path = my_graph.shortestPath(self.origin_p.id, self.destination_p.id)
            for i in shortest_path:
                self.map_widget.set_polygon(self.polygons[i].coords, outline_color='orange', fill_color='yellow')
            for i, value in enumerate(shortest_path[:-1]):
                self.map_widget.set_path(my_graph.routes_matrix[shortest_path[i]][shortest_path[i+1]].coords, color='yellow', width=3)
        else:
            msg = messagebox.showinfo("error", "please select origin and destination polygons")

    # when click on clear route button, origin & destination polygons' selections clear, and so as path (if calculated)
    def clear_route(self):
        self.show_polygons()
        self.show_routes()
        self.origin_p = None
        self.destination_p = None

    # when click on close program button,
    def close_program(self):
        self.destroy()

    def run(self):        
        self.mainloop()