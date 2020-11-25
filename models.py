from math import sqrt
from tqdm import tqdm


class Node:
    def __init__(self, point, dim):
        self.start = point  # Point
        self.dim = dim  # Vector

        self.vertices = [
            self.start.move(Vector(0, 0, 0)),
            self.start.move(Vector(dim.x, 0, 0)),
            self.start.move(Vector(0, 0, dim.z)),
            self.start.move(Vector(dim.x, 0, dim.z)),

            self.start.move(Vector(0, dim.y, 0)),
            self.start.move(Vector(dim.x, dim.y, 0)),
            self.start.move(Vector(0, dim.y, dim.z)),
            self.start.move(Vector(dim.x, dim.y, dim.z))
        ]

        self.is_leaf = True  # kazdy węzeł na początku jest liściem
        self.branches = [None] * 8

    def split(self):
        """Podziel węzeł na osiem"""
        self.is_leaf = False

        new_dim = Vector(self.dim.x / 2, self.dim.y / 2, self.dim.z / 2)

        self.branches[0b000] = Node(self.start.move(Vector(0, 0, 0)), new_dim)
        self.branches[0b001] = Node(self.start.move(Vector(new_dim.x, 0, 0)), new_dim)
        self.branches[0b010] = Node(self.start.move(Vector(0, 0, new_dim.z)), new_dim)
        self.branches[0b011] = Node(self.start.move(Vector(new_dim.x, 0, new_dim.z)), new_dim)

        self.branches[0b100] = Node(self.start.move(Vector(0, new_dim.y, 0)), new_dim)
        self.branches[0b101] = Node(self.start.move(Vector(new_dim.x, new_dim.y, 0)), new_dim)
        self.branches[0b110] = Node(self.start.move(Vector(0, new_dim.y, new_dim.z)), new_dim)
        self.branches[0b111] = Node(self.start.move(Vector(new_dim.x, new_dim.y, new_dim.z)), new_dim)

    def can_be_split(self, condition, object):
        c1 = (self.dim.x / 2) * (self.dim.y / 2) * (self.dim.z / 2) >= condition
        c2 = self.check_object(object)
        return c1 and c2

    def check_object(self, object):
        c = self.start.move(Vector(self.dim.x / 2, self.dim.y / 2, self.dim.z / 2))
        step = Vector(-c.x, -c.y, -c.z)

        for triangle in object.triangles:
            v0 = triangle.v1.move(step)
            v1 = triangle.v2.move(step)
            v2 = triangle.v3.move(step)

            if not self.check_AABB(v0, v1, v2):
                continue

            if not self.check_plane(triangle):
                continue

            if not self.final_check(v0, v1, v2):
                continue

            return True
        return False

    def check_AABB(self, v0, v1, v2):
        x_min = min(v0.x, v1.x, v2.x)
        x_max = max(v0.x, v1.x, v2.x)
        if x_max < -self.dim.x / 2 or x_min > self.dim.x / 2:
            return False

        y_min = min(v0.y, v1.y, v2.y)
        y_max = max(v0.y, v1.y, v2.y)
        if y_max < -self.dim.y / 2 or y_min > self.dim.y / 2:
            return False

        z_min = min(v0.z, v1.z, v2.z)
        z_max = max(v0.z, v1.z, v2.z)
        if z_max < -self.dim.z / 2 or z_min > self.dim.z / 2:
            return False

        return True

    def check_plane(self, triangle):
        def condition(p1, p2):
            return (triangle.n.dot_product(p1) + d) * (triangle.n.dot_product(p2) + d) <= 0

        d = (-1) * triangle.n.dot_product(triangle.v1)
        pairs = [
            [self.vertices[0], self.vertices[7]],
            [self.vertices[1], self.vertices[6]],
            [self.vertices[2], self.vertices[5]],
            [self.vertices[3], self.vertices[4]],
        ]

        for v1, v2 in pairs:
            if condition(v1, v2):
                return True

        return False

    def final_check(self, v0, v1, v2):
        es = [Vector(1, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1)]
        fs = [Vector(v0, v1), Vector(v1, v2), Vector(v2, v0)]
        for e in es:
            for f in fs:
                a = e.cross_product(f)
                p0 = a.dot_product(v0)
                p1 = a.dot_product(v1)
                p2 = a.dot_product(v2)
                r = self.dim.x * abs(a.x) + self.dim.y * abs(a.y) + self.dim.z * abs(a.z)
                if min(p0, p1, p2) > r or max(p0, p1, p2) < -r:
                    return False
        return True

    def get_external_edges(self):
        return [
            [self.vertices[0], self.vertices[1]],
            [self.vertices[1], self.vertices[3]],
            [self.vertices[3], self.vertices[2]],
            [self.vertices[2], self.vertices[0]],

            [self.vertices[0], self.vertices[4]],
            [self.vertices[1], self.vertices[5]],
            [self.vertices[3], self.vertices[7]],
            [self.vertices[2], self.vertices[6]],

            [self.vertices[4], self.vertices[5]],
            [self.vertices[5], self.vertices[7]],
            [self.vertices[7], self.vertices[6]],
            [self.vertices[6], self.vertices[4]]
        ]

    def get_inner_edges(self):
        p01 = self.vertices[0].move(Vector(self.dim.x / 2, 0, 0))
        p13 = self.vertices[1].move(Vector(0, 0, self.dim.z / 2))
        p32 = self.vertices[2].move(Vector(self.dim.x / 2, 0, 0))
        p20 = self.vertices[0].move(Vector(0, 0, self.dim.z / 2))
        p04 = self.vertices[0].move(Vector(0, self.dim.y / 2, 0))
        p15 = self.vertices[1].move(Vector(0, self.dim.y / 2, 0))
        p37 = self.vertices[3].move(Vector(0, self.dim.y / 2, 0))
        p26 = self.vertices[2].move(Vector(0, self.dim.y / 2, 0))
        p45 = self.vertices[4].move(Vector(self.dim.x / 2, 0, 0))
        p57 = self.vertices[5].move(Vector(0, 0, self.dim.z / 2))
        p76 = self.vertices[6].move(Vector(self.dim.x / 2, 0, 0))
        p64 = self.vertices[4].move(Vector(0, 0, self.dim.z / 2))

        p0145 = self.vertices[0].move(Vector(self.dim.x / 2, self.dim.y / 2, 0))
        p1375 = self.vertices[1].move(Vector(0, self.dim.y / 2, self.dim.z / 2))
        p2376 = self.vertices[2].move(Vector(self.dim.x / 2, self.dim.y / 2, 0))
        p0264 = self.vertices[0].move(Vector(0, self.dim.y / 2, self.dim.z / 2))
        p0132 = self.vertices[0].move(Vector(self.dim.x / 2, 0, self.dim.z / 2))
        p4576 = self.vertices[4].move(Vector(self.dim.x / 2, 0, self.dim.z / 2))

        return [
            [p01, p32], [p32, p76], [p76, p45], [p45, p01],
            [p04, p15], [p15, p37], [p37, p26], [p26, p04],
            [p20, p13], [p13, p57], [p57, p64], [p64, p20],
            [p0132, p4576], [p0145, p2376], [p0264, p1375]
        ]

    def point_in_node(self, point):
        if self.start.x < self.vertices[-1].x:
            x = self.start.x <= point.x <= self.vertices[-1].x
        else:
            x = self.vertices[-1].x <= point.x <= self.start.x

        if self.start.y < self.vertices[-1].y:
            y = self.start.y <= point.y <= self.vertices[-1].y
        else:
            y = self.vertices[-1].y <= point.y <= self.start.y

        if self.start.z < self.vertices[-1].z:
            z = self.start.z <= point.z <= self.vertices[-1].z
        else:
            z = self.vertices[-1].z <= point.z <= self.start.z

        return x and y and z

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

    def dot_product(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross_product(self, other):
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def __eq__(self, obj):
        return isinstance(obj, Vector) and obj.x == self.x and obj.y == self.y and obj.z == self.z

    def __str__(self):
        return f'[{self.x}, {self.y}, {self.z}]'


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
