from functions import dot_product
from math import sqrt
from tqdm import tqdm


class Node:
    def __init__(self, point, dim):
        self.start = point  # Point
        self.dim = dim  # Vector

        self.vertices = [
            point,
            Point(point.x + dim.x, point.y, point.z),
            Point(point.x, point.y, point.z + dim.z),
            Point(point.x + dim.x, point.y, point.z + dim.z),
            Point(point.x, point.y + dim.y, point.z),
            Point(point.x + dim.x, point.y + dim.y, point.z),
            Point(point.x, point.y + dim.y, point.z + dim.z),
            Point(point.x + dim.x, point.y + dim.y, point.z + dim.z)
        ]

        self.edges = [
            Edge(self.vertices[0], self.vertices[1]),
            Edge(self.vertices[1], self.vertices[3]),
            Edge(self.vertices[3], self.vertices[2]),
            Edge(self.vertices[2], self.vertices[0]),

            Edge(self.vertices[0], self.vertices[4]),
            Edge(self.vertices[1], self.vertices[5]),
            Edge(self.vertices[3], self.vertices[7]),
            Edge(self.vertices[2], self.vertices[6]),

            Edge(self.vertices[4], self.vertices[5]),
            Edge(self.vertices[5], self.vertices[7]),
            Edge(self.vertices[7], self.vertices[6]),
            Edge(self.vertices[6], self.vertices[4])
        ]

        self.walls = [
            NodeWall(
                Vector(self.vertices[2], self.vertices[0]),
                Vector(self.vertices[1], self.vertices[0]),
                self.vertices[0]
            ),
            NodeWall(
                Vector(self.vertices[5], self.vertices[1]),
                Vector(self.vertices[3], self.vertices[1]),
                self.vertices[1]
            ),
            NodeWall(
                Vector(self.vertices[7], self.vertices[3]),
                Vector(self.vertices[2], self.vertices[3]),
                self.vertices[3]
            ),
            NodeWall(
                Vector(self.vertices[6], self.vertices[2]),
                Vector(self.vertices[0], self.vertices[2]),
                self.vertices[2]
            ),
            NodeWall(
                Vector(self.vertices[4], self.vertices[0]),
                Vector(self.vertices[1], self.vertices[0]),
                self.vertices[0]
            ),
            NodeWall(
                Vector(self.vertices[6], self.vertices[4]),
                Vector(self.vertices[5], self.vertices[4]),
                self.vertices[4]
            )
        ]

        self.is_leaf = True  # kazdy węzeł na początku jest liściem
        self.branches = [None] * 8

    def __str__(self):
        """Reprezentacja pojedynczego węzła jako jego punkt początkowy; debug only."""
        return f'{self.start} -> {self.dim.x}, {self.dim.y}, {self.dim.z}'

    def can_be_split(self, condition, object):
        return (self.dim.x / 2) * (self.dim.y / 2) * (self.dim.z / 2) >= condition and self.check_object(object)

    def point_in_node(self, point):
        x = self.start.x <= point.x <= self.start.x + self.dim.x
        y = self.start.y <= point.y <= self.start.y + self.dim.y
        z = self.start.z <= point.z <= self.start.z + self.dim.z
        return x and y and z

    def check_object(self, object):
        if object is None:
            return True  # debug only - in this case there is no stl object to compare

        # TODO: splitting if there is object in the node
        # case 1: vertex
        for vertex in object.vertices:
            if self.point_in_node(vertex):
                return True

        # case 2: edge
        for edge in object.edges:
            for wall in self.walls:
                check_a = dot_product(wall.n, edge.a) + wall.d
                check_b = dot_product(wall.n, edge.b) + wall.d
                if check_a == 0:
                    if self.point_in_node(edge.a):
                        return True
                if check_b == 0:
                    if self.point_in_node(edge.b):
                        return True
                if check_a * check_b < 0:
                    # print("Checking...")
                    w = (dot_product(wall.n, edge.b) + wall.d) / dot_product(wall.n, edge.vector)
                    new_point = Point(
                        edge.b.x - edge.vector.x * w,
                        edge.b.y - edge.vector.y * w,
                        edge.b.z - edge.vector.z * w,
                    )
                    if self.point_in_node(new_point):
                        # print("True")
                        return True

        # case 3: triangle

        return False  # TODO: change to False when done

    def split(self):
        """Podziel węzeł na osiem"""
        self.is_leaf = False

        dim = Vector(self.dim.x / 2, self.dim.y / 2, self.dim.z / 2)

        self.branches[0b000] = Node(self.start.move(Vector(0, 0, 0)), dim)
        self.branches[0b001] = Node(self.start.move(Vector(dim.x, 0, 0)), dim)
        self.branches[0b010] = Node(self.start.move(Vector(0, 0, dim.z)), dim)
        self.branches[0b011] = Node(self.start.move(Vector(dim.x, 0, dim.z)), dim)

        self.branches[0b100] = Node(self.start.move(Vector(0, dim.y, 0)), dim)
        self.branches[0b101] = Node(self.start.move(Vector(dim.x, dim.y, 0)), dim)
        self.branches[0b110] = Node(self.start.move(Vector(0, dim.y, dim.z)), dim)
        self.branches[0b111] = Node(self.start.move(Vector(dim.x, dim.y, dim.z)), dim)

    def find_point(self, point):
        if self is None or self.is_leaf:
            return self
        else:
            x = "1" if point.x > self.start.x + self.dim.x / 2 else "0"
            y = "1" if point.y > self.start.y + self.dim.y / 2 else "0"
            z = "1" if point.z > self.start.z + self.dim.z / 2 else "0"
            binary = "0b" + x + y + z
            return self.branches[int(binary, 2)].find_point(point)


class Vector:
    def __init__(self, *args):
        if len(args) == 3:  # there are three numbers
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]
        elif len(args) == 2:  # there are two points
            self.x = args[1].x - args[0].x
            self.y = args[1].y - args[0].y
            self.z = args[1].z - args[0].z

    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __eq__(self, obj):
        return isinstance(obj, Vector) and obj.x == self.x and obj.y == self.y and obj.z == self.z

    def __str__(self):
        return f'[{self.x}, {self.y}, {self.z}]'


class NodeWall:
    def __init__(self, v1, v2, p):
        self.v1 = v1  # vector
        self.v2 = v2  # vector
        self.n = self.get_n()  # vector
        self.d = self.get_d(p)  # float

    def get_n(self):
        cross_product = Vector(
            self.v1.y * self.v2.z - self.v2.y * self.v1.z,
            self.v2.x * self.v1.z - self.v1.x * self.v2.z,
            self.v1.x * self.v2.y - self.v2.x * self.v1.y
        )
        return Vector(
            cross_product.x / cross_product.length(),
            cross_product.y / cross_product.length(),
            cross_product.z / cross_product.length()
        )

    def get_d(self, p):
        return dot_product(self.v1, p)


def get_edges_from_triangle(triangle):
    return [
        Edge(triangle.v1, triangle.v2),
        Edge(triangle.v2, triangle.v3),
        Edge(triangle.v3, triangle.v1),
    ]


class Point:
    def __init__(self, x, y, z):
        self.x = x  # int
        self.y = y  # int
        self.z = z  # int

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __eq__(self, obj):
        return isinstance(obj, Point) and obj.x == self.x and obj.y == self.y and obj.z == self.z

    def __hash__(self):
        return hash(self.x) * hash(self.y) * hash(self.z)

    def move(self, vector):
        return Point(
            self.x + vector.x,
            self.y + vector.y,
            self.z + vector.z,
        )


class Edge:
    def __init__(self, p1, p2):
        self.a = p1  # Point
        self.b = p2  # Point
        self.vector = Vector(p1, p2)

    def __str__(self):
        return f"{self.a} -> {self.b}"

    def __eq__(self, obj):
        first = obj.a == self.a and obj.b == self.b
        second = obj.b == self.a and obj.a == self.b
        return (first or second) and isinstance(obj, Edge)

    def __hash__(self):
        return hash(self.a) * hash(self.b)


class Triangle:
    def __init__(self, v1, v2, v3, n):
        # each triangle has three vertices and a normal
        self.v1 = v1  # Point
        self.v2 = v2  # Point
        self.v3 = v3  # Point
        self.n = n  # vector

    def __str__(self):
        return f"{self.v1},       {self.v2},       {self.v3}       N = {self.n}"

    def get_edges(self):
        return [
            Edge(self.v1, self.v2),
            Edge(self.v2, self.v3),
            Edge(self.v3, self.v1)
        ]


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
            print(f'> Parse {self.filename}...')
            for line in tqdm(file.readlines()):
                if "normal" in line:
                    s = line.split()
                    n = Vector(float(s[2]), float(s[3]), float(s[4]))
                    self.normal_array.append(n)
                if "vertex" in line:
                    s = line.split()
                    p = Point(float(s[1]), float(s[2]), float(s[3]))
                    self.vertex_array.append(p)

        assert len(self.normal_array) * 3 == len(self.vertex_array)

    def get_triangles(self):
        triangles = []

        print('> Get triangles...')
        for i, normal in tqdm(enumerate(self.normal_array)):
            triangle = Triangle(
                self.vertex_array[3 * i],
                self.vertex_array[3 * i + 1],
                self.vertex_array[3 * i + 2],
                normal
            )

            triangles.append(triangle)

        return triangles

    def get_vertices(self):
        print('> Get vertices...')
        return set(self.vertex_array)

    def get_edges(self):
        edges = []

        print('> Get edges...')
        for triangle in tqdm(self.triangles):
            edges += triangle.get_edges()

        return set(edges)
