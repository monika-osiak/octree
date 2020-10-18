class Node:
    def __init__(self, point, dim):
        """Zwróć nowy węzeł o początku w punkcie (x, y, z) i bokach dx, dy, dz"""
        self.x = point[0]
        self.y = point[1]
        self.z = point[2]
        self.dx = dim[0]
        self.dy = dim[1]
        self.dz = dim[2]

        self.is_leaf = True  # kazdy węzeł na początku jest liściem
        self.branches = [None] * 8

    def __str__(self):
        """Reprezentacja pojedynczego węzła jako jego punkt początkowy; debug only."""
        return f'({self.x}, {self.y}, {self.z}) -> {self.dx}, {self.dy}, {self.dz}'

    def can_be_split(self, condition, object):
        return (self.dx / 2) * (self.dy / 2) * (self.dz / 2) >= condition and self.check_object(object)

    def vertex_in_node(self, vertex):
        x = self.x <= vertex.x <= self.x + self.dx
        y = self.y <= vertex.y <= self.y + self.dy
        z = self.z <= vertex.z <= self.z + self.dz
        return x and y and z

    def check_object(self, object):
        if object is None:
            return True  # debug only - in this case there is no stl object to compare

        # TODO: splitting if there is object in the node
        # case 1: vertex
        for v in object.vertices:
            if self.vertex_in_node(v):
                return True

        # case 2: edge

        # case 3: triangle

        return True  # TODO: change to False when done

    def split(self):
        """Podziel węzeł na osiem"""
        self.is_leaf = False

        dim = [self.dx / 2, self.dy / 2, self.dz / 2]

        self.branches[0b000] = Node([self.x, self.y, self.z], dim)
        self.branches[0b001] = Node([self.x + self.dx / 2, self.y, self.z], dim)
        self.branches[0b010] = Node([self.x, self.y, self.z + self.dz / 2], dim)
        self.branches[0b011] = Node([self.x + self.dx / 2, self.y, self.z + self.dz / 2], dim)
        self.branches[0b100] = Node([self.x, self.y + self.dy / 2, self.z], dim)
        self.branches[0b101] = Node([self.x + self.dx / 2, self.y + self.dy / 2, self.z], dim)
        self.branches[0b110] = Node([self.x, self.y + self.dy / 2, self.z + self.dz / 2], dim)
        self.branches[0b111] = Node([self.x + self.dx / 2, self.y + self.dy / 2, self.z + self.dz / 2], dim)

    def find_point(self, point):
        if self is None or self.is_leaf:
            return self
        else:
            x = "1" if point[0] > self.x + self.dx / 2 else "0"
            y = "1" if point[1] > self.y + self.dy / 2 else "0"
            z = "1" if point[2] > self.z + self.dz / 2 else "0"
            binary = "0b" + x + y + z
            return self.branches[int(binary, 2)].find_point(point)


class Triangle:
    def __init__(self, v1, v2, v3, normal):
        # each triangle has three vertices and a normal
        self.v1 = v1  # Vertex
        self.v2 = v2  # Vertex
        self.v3 = v3  # Vertex
        self.normal = normal  # list

    def __str__(self):
        return f"{self.v1},       {self.v2},       {self.v3}       N = {self.normal}"


class Vertex:
    def __init__(self, x, y, z):
        self.x = x  # int
        self.y = y  # int
        self.z = z  # int

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __eq__(self, obj):
        return isinstance(obj, Vertex) and obj.x == self.x and obj.y == self.y and obj.z == self.z

    def __hash__(self):
        return hash(self.x) * hash(self.y) * hash(self.z)


def get_edges_from_triangle(triangle):
    return [
        Edge(triangle.v1, triangle.v2),
        Edge(triangle.v2, triangle.v3),
        Edge(triangle.v3, triangle.v1),
    ]


class Edge:
    def __init__(self, v1, v2):
        self.v1 = v1  # Vertex
        self.v2 = v2  # Vertex

    def __str__(self):
        return f"{self.v1} -> {self.v2}"

    def __eq__(self, obj):
        first = obj.v1 == self.v1 and obj.v2 == self.v2
        second = obj.v2 == self.v1 and obj.v1 == self.v2
        return (first or second) and isinstance(obj, Edge)

    def __hash__(self):
        return hash(self.v1) * hash(self.v2)


class STL:
    def __init__(self, filename):
        self.filename = filename
        self.normal_array = []
        self.vertex_array = []

        self.parse_file()

        self.triangles = self.get_triangles()
        self.vertices = self.get_vertices()
        self.edges = self.get_edges()

    def parse_file(self):
        with open(self.filename) as file:
            for line in file.readlines():
                if "normal" in line:
                    s = line.split()
                    self.normal_array.append([s[2], s[3], s[4]])
                if "vertex" in line:
                    s = line.split()
                    self.vertex_array.append(Vertex(s[1], s[2], s[3]))

        assert len(self.normal_array) * 3 == len(self.vertex_array)

    def get_triangles(self):
        triangles = []

        for i, normal in enumerate(self.normal_array):
            triangle = Triangle(
                self.vertex_array[3 * i],
                self.vertex_array[3 * i + 1],
                self.vertex_array[3 * i + 2],
                normal
            )

            triangles.append(triangle)

        return triangles

    def get_vertices(self):
        return set(self.vertex_array)

    def get_edges(self):
        edges = []

        for triangle in self.triangles:
            edges += get_edges_from_triangle(triangle)

        return set(edges)
