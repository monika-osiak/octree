from stl_models import Edge, Vertex
from functions import length, dot_product


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

        self.v = self.get_vertices()  # list
        self.e = self.get_edges()  # list
        self.w = self.get_walls()  # list

    def __str__(self):
        """Reprezentacja pojedynczego węzła jako jego punkt początkowy; debug only."""
        return f'({self.x}, {self.y}, {self.z}) -> {self.dx}, {self.dy}, {self.dz}'

    def get_vertices(self):
        return [
            Vertex(self.x, self.y, self.z),
            Vertex(self.x + self.dx, self.y, self.z),
            Vertex(self.x, self.y, self.z + self.dz),
            Vertex(self.x + self.dx, self.y, self.z + self.dz),
            Vertex(self.x, self.y + self.dy, self.z),
            Vertex(self.x + self.dx, self.y + self.dy, self.z),
            Vertex(self.x, self.y + self.dy, self.z + self.dz),
            Vertex(self.x + self.dx, self.y + self.dy, self.z + self.dz)
        ]

    def get_edges(self):
        return [
            Edge(self.v[0], self.v[1]), Edge(self.v[1], self.v[3]),
            Edge(self.v[3], self.v[2]), Edge(self.v[2], self.v[0]),
            Edge(self.v[0], self.v[4]), Edge(self.v[1], self.v[5]),
            Edge(self.v[3], self.v[7]), Edge(self.v[2], self.v[6]),
            Edge(self.v[4], self.v[5]), Edge(self.v[5], self.v[7]),
            Edge(self.v[7], self.v[6]), Edge(self.v[6], self.v[4])
        ]

    def get_walls(self):
        return [
            NodeWall(
                Vector(self.v[2].x - self.v[0].x, self.v[2].y - self.v[0].y, self.v[2].z - self.v[0].z),
                Vector(self.v[1].x - self.v[0].x, self.v[1].y - self.v[0].y, self.v[1].z - self.v[0].z),
                self.v[0]
            ),
            NodeWall(
                Vector(self.v[5].x - self.v[1].x, self.v[5].y - self.v[1].y, self.v[5].z - self.v[1].z),
                Vector(self.v[3].x - self.v[1].x, self.v[3].y - self.v[1].y, self.v[3].z - self.v[1].z),
                self.v[1]
            ),
            NodeWall(
                Vector(self.v[7].x - self.v[3].x, self.v[7].y - self.v[3].y, self.v[7].z - self.v[3].z),
                Vector(self.v[2].x - self.v[3].x, self.v[2].y - self.v[3].y, self.v[2].z - self.v[3].z),
                self.v[3]
            ),
            NodeWall(
                Vector(self.v[6].x - self.v[2].x, self.v[6].y - self.v[2].y, self.v[6].z - self.v[2].z),
                Vector(self.v[0].x - self.v[2].x, self.v[0].y - self.v[2].y, self.v[0].z - self.v[2].z),
                self.v[2]
            ),
            NodeWall(
                Vector(self.v[4].x - self.v[0].x, self.v[4].y - self.v[0].y, self.v[4].z - self.v[0].z),
                Vector(self.v[1].x - self.v[0].x, self.v[1].y - self.v[0].y, self.v[1].z - self.v[0].z),
                self.v[0]
            ),
            NodeWall(
                Vector(self.v[6].x - self.v[4].x, self.v[6].y - self.v[4].y, self.v[6].z - self.v[4].z),
                Vector(self.v[5].x - self.v[4].x, self.v[5].y - self.v[4].y, self.v[5].z - self.v[4].z),
                self.v[4]
            ),
        ]

    def can_be_split(self, condition, object):
        return ((self.dx / 2) * (self.dy / 2) * (self.dz / 2) >= condition) and (self.check_object(object))

    def vertex_in_node(self, vertex):
        # print(f'Check {vertex} in <{self.x}; {self.x + self.dx}>, <{self.y}; {self.y + self.dy}>, <{self.z}; {self.z + self.dz}>, ')
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
        for e in object.edges:
            edge_vector = Vector(
                e.v2.x - e.v1.x,
                e.v2.y - e.v1.y,
                e.v2.z - e.v1.z,
            )
            for wall in self.w:
                check_a = dot_product(wall.n, e.v1) + wall.d
                check_b = dot_product(wall.n, e.v2) + wall.d
                if check_a == 0:
                    if self.vertex_in_node(e.v1):
                        return True
                if check_b == 0:
                    if self.vertex_in_node(e.v2):
                        return True
                if check_a * check_b < 0:
                    # print("Checking...")
                    W = (dot_product(wall.n, e.v2) + wall.d) / dot_product(wall.n, edge_vector)
                    P = Vertex(
                        e.v2.x - edge_vector.x * W,
                        e.v2.y - edge_vector.y * W,
                        e.v2.z - edge_vector.z * W,
                    )
                    if self.vertex_in_node(P):
                        # print("True")
                        return True

        # case 3: triangle

        return False  # TODO: change to False when done

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


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class NodeWall:
    def __init__(self, v1, v2, p):
        self.v1 = v1  # vector
        self.v2 = v2  # vector
        self.n = self.get_normal()  # vector
        self.d = self.get_d(p)  # float

    def get_normal(self):
        v = Vector(
            self.v1.y * self.v2.z - self.v2.y * self.v1.z,
            self.v2.x * self.v1.z - self.v1.x * self.v2.z,
            self.v1.x * self.v2.y - self.v2.x * self.v1.y
        )
        l = length(v)
        return Vector(v.x/l, v.y/l, v.z/l)

    def get_d(self, p):
        return dot_product(self.v1, p)
