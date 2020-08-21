class Node:
    def __init__(self, tree, x, y, z, level=0):
        """Zwróć nowy węzeł o początku w punkcie (x, y, z) i bokach dx, dy, dz"""
        self.x = x
        self.y = y
        self.z = z
        self.level = level
        self.is_leaf = True  # kazdy węzeł na początku jest liściem
        self.branches = [None] * 8
        self.tree = tree

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
        return "({}, {}, {})\t -> {}, {}, {}".format(
            self.x,
            self.y,
            self.z,
            self.get_dx(),
            self.get_dy(),
            self.get_dz())

    def get_dx(self):
        return self.tree.dx / (2 ** self.level)

    def get_dy(self):
        return self.tree.dy / (2 ** self.level)

    def get_dz(self):
        return self.tree.dz / (2 ** self.level)

    def split(self):
        """Podziel węzeł na osiem"""
        self.is_leaf = False

        self.branches[0] = Node(
            self.tree,
            self.x,
            self.y,
            self.z,
            self.level + 1
        )

        self.branches[1] = Node(
            self.tree,
            self.x + self.get_dx() / 2,
            self.y,
            self.z,
            self.level + 1
        )

        self.branches[2] = Node(
            self.tree,
            self.x,
            self.y,
            self.z + self.get_dz() / 2,
            self.level + 1
        )

        self.branches[3] = Node(
            self.tree,
            self.x + self.get_dx() / 2,
            self.y,
            self.z + self.get_dz() / 2,
            self.level + 1
        )

        self.branches[4] = Node(
            self.tree,
            self.x,
            self.y + self.get_dy() / 2,
            self.z,
            self.level + 1
        )

        self.branches[5] = Node(
            self.tree,
            self.x + self.get_dx() / 2,
            self.y + self.get_dy() / 2,
            self.z,
            self.level + 1
        )

        self.branches[6] = Node(
            self.tree,
            self.x,
            self.y + self.get_dy() / 2,
            self.z + self.get_dz() / 2,
            self.level + 1
        )

        self.branches[7] = Node(
            self.tree,
            self.x + self.get_dx() / 2,
            self.y + self.get_dy() / 2,
            self.z + self.get_dz() / 2,
            self.level + 1
        )


class Octree:
    def __init__(self, dx, dy, dz):
        """Zwróć nowe drzewo o początku w punkcie (0,0,0) i wymiarach dz, dy, dz"""
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.root = self.add_node(self, 0, 0, 0)

    def add_node(self, x, y, z, level=0):
        """Zwróć nowy węzeł"""
        return Node(self, x, y, z, level)


if __name__ == "__main__":
    octree = Octree(10, 10, 10)
    print(octree.root)
    octree.root.split()
    for child in octree.root.branches:
        print(child)
