from tqdm import tqdm


def get_edges_from_triangle(triangle):
    return [
        Edge(triangle.v1, triangle.v2),
        Edge(triangle.v2, triangle.v3),
        Edge(triangle.v3, triangle.v1),
    ]


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


class Triangle:
    def __init__(self, v1, v2, v3, normal):
        # each triangle has three vertices and a normal
        self.v1 = v1  # Vertex
        self.v2 = v2  # Vertex
        self.v3 = v3  # Vertex
        self.normal = normal  # list

    def __str__(self):
        return f"{self.v1},       {self.v2},       {self.v3}       N = {self.normal}"


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
                    self.normal_array.append([
                        float(s[2]),
                        float(s[3]),
                        float(s[4])
                    ])
                if "vertex" in line:
                    s = line.split()
                    self.vertex_array.append(Vertex(
                        float(s[1]),
                        float(s[2]),
                        float(s[3])
                    ))

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
            edges += get_edges_from_triangle(triangle)

        return set(edges)
