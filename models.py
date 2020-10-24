from stl_models import Edge, Vertex


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

    def get_edges(self):
        v1 = Vertex(self.x, self.y, self.z)
        v2 = Vertex(self.x + self.dx, self.y, self.z)
        v3 = Vertex(self.x, self.y, self.z + self.dz)
        v4 = Vertex(self.x + self.dx, self.y, self.z + self.dz)
        v5 = Vertex(self.x, self.y + self.dy, self.z)
        v6 = Vertex(self.x + self.dx, self.y + self.dy, self.z)
        v7 = Vertex(self.x, self.y + self.dy, self.z + self.dz)
        v8 = Vertex(self.x + self.dx, self.y + self.dy, self.z + self.dz)

        result = [
            Edge(v1, v2), Edge(v2, v4), Edge(v4, v3), Edge(v3, v1),
            Edge(v1, v5), Edge(v2, v6), Edge(v4, v8), Edge(v3, v7),
            Edge(v5, v6), Edge(v6, v8), Edge(v8, v7), Edge(v7, v5)
        ]

        return result

    def can_be_split(self, condition, object):
        return ((self.dx / 2) * (self.dy / 2) * (self.dz / 2) >= condition) and (self.check_object(object))

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
