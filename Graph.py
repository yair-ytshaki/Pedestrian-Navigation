from Polyline import Polyline
from Route import Route
from collections import deque

class Graph():
    #contains list of Routes and list of Polygons as a base to create adjacency matrix
    def __init__(self, routes, polygons):
        """
        :param routes, polygons: list of Routes and Polygons to create adjacency matrix and a routes' matrix.
        routes' matrix contains routes of every non-empty cell in the created adjacency matrix, respectively
        """
        self.routes = routes
        self.polygons = polygons
        self.adj_matrix, self.routes_matrix = self.adjacency_matrix()

    def adjacency_matrix (self):
        """
        :return: the adjacency matrix and the routes' matrix, as explained above
        """
        matrix = [[-1.0 for _ in range(len(self.polygons))] for _ in range(len(self.polygons))]
        routes_mat = [[None for _ in range(len(self.polygons))] for _ in range(len(self.polygons))]
        for i in range(len(self.polygons)):
            for j in range(len(self.polygons)):
                for r in self.routes:
                    if(r.s_polygon.id == self.polygons[i].id and r.t_polygon.id == self.polygons[j].id
                        or r.s_polygon.id == self.polygons[j].id and r.t_polygon.id == self.polygons[i].id
                    ):
                        routes_mat[i][j] = r
                        matrix[i][j]=r.route_length()
        return matrix, routes_mat

    def shortestPath (self, start, end):
        """
        :param start, end: user's selected origin and destination polygons to calculate the shortest path between them.
        :return: a float-instance distance of the shortest path, and a list of every path's assemble polygons, by order.
        """
        num_nodes = len(self.polygons)
        # Create a list to store the shortest distance from start to each node
        distance = [float('inf')] * num_nodes
        distance[start] = 0
        # Create a list to store the previous vertex of each node in the shortest path
        previous_vertex = [None] * num_nodes #list
        # Create a list to keep track of visited nodes
        visited = [False] * num_nodes
        # Create a double-ended queue (deque) to store nodes to be processed
        queue = deque()
        queue.append(start)

        while queue:
            current_node = queue.popleft()
            visited[current_node] = True
            # Check all the neighbors of the current node
            for neighbor in range(num_nodes):
                if self.adj_matrix[current_node][neighbor] > 0:  # There is an edge between the current node and the neighbor
                    if not visited[neighbor]:
                        new_distance = distance[current_node] + self.adj_matrix[current_node][neighbor]
                        if new_distance < distance[neighbor]:
                            distance[neighbor] = new_distance
                            previous_vertex[neighbor] = current_node
                            queue.append(neighbor)

        # Build the shortest path from start to end by backtracking from the end node
        path = []
        current_node = end
        while current_node is not None:
            path.insert(0, current_node) # insert in the first index of the list (insert node's number), and push right the others
            current_node = previous_vertex[current_node]

        return distance[end], path