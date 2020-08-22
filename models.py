class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'


class Scene:
    def __init__(self, dx, dy, dz):
        self.dx = dx
        self.dy = dy
        self.dz = dz


class Node:
    def __init__(self, scene, x, y, z, level=0):
        """Zwróć nowy węzeł o początku w punkcie (x, y, z) i bokach dx, dy, dz"""
        self.vertex = Point(x, y, z)
        self.level = level
        self.is_leaf = True  # kazdy węzeł na początku jest liściem
        self.branches = [None] * 8
        self.scene = scene

        """
    Numeracja gałęzi wynika z ponizszego podziału.
    Wartości binarne odpowiadają (x,y,z).
    
    Dzielimy sześcian w połowie wzdłuz płaszczyzny X:
        Y < połowa => 0
        w p.p. => 1

    Reszta analogicznie

    ---------------------
    |         |         |
    | 110 = 6 | 111 = 7 |
    |         |         |
    ---------------------
    |         |         |
    | 100 = 4 | 101 = 5 |
    |         |         |
    ---------------------    Rys. 1. Górna część sześcianu

    ---------------------
    |         |         |
    | 010 = 2 | 011 = 3 |
    |         |         |
    ---------------------
    |         |         |
    | 000 = 0 | 001 = 1 |
    |         |         |
    ---------------------    Rys. 2. Dolna część sześcianu
    """

    def __str__(self):
        """Reprezentacja pojedynczego węzła jako jego punkt początkowy; debug only."""
        return f'{self.vertex} -> {self.get_dx()}, {self.get_dy()}, {self.get_dz()}'

    def get_dx(self):
        return self.scene.dx / (2 ** self.level)

    def get_dy(self):
        return self.scene.dy / (2 ** self.level)

    def get_dz(self):
        return self.scene.dz / (2 ** self.level)

    def can_be_split(self, condition):
        return self.get_dx() > condition and self.get_dy() > condition and self.get_dz() > condition

    def split(self):
        """Podziel węzeł na osiem"""
        self.is_leaf = False

        self.branches[0] = Node(
            self.scene,
            self.vertex.x,
            self.vertex.y,
            self.vertex.z,
            self.level + 1
        )

        self.branches[1] = Node(
            self.scene,
            self.vertex.x + self.get_dx() / 2,
            self.vertex.y,
            self.vertex.z,
            self.level + 1
        )

        self.branches[2] = Node(
            self.scene,
            self.vertex.x,
            self.vertex.y,
            self.vertex.z + self.get_dz() / 2,
            self.level + 1
        )

        self.branches[3] = Node(
            self.scene,
            self.vertex.x + self.get_dx() / 2,
            self.vertex.y,
            self.vertex.z + self.get_dz() / 2,
            self.level + 1
        )

        self.branches[4] = Node(
            self.scene,
            self.vertex.x,
            self.vertex.y + self.get_dy() / 2,
            self.vertex.z,
            self.level + 1
        )

        self.branches[5] = Node(
            self.scene,
            self.vertex.x + self.get_dx() / 2,
            self.vertex.y + self.get_dy() / 2,
            self.vertex.z,
            self.level + 1
        )

        self.branches[6] = Node(
            self.scene,
            self.vertex.x,
            self.vertex.y + self.get_dy() / 2,
            self.vertex.z + self.get_dz() / 2,
            self.level + 1
        )

        self.branches[7] = Node(
            self.scene,
            self.vertex.x + self.get_dx() / 2,
            self.vertex.y + self.get_dy() / 2,
            self.vertex.z + self.get_dz() / 2,
            self.level + 1
        )
