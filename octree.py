class Node:
    def __init__(self, x, y, z, dx, dy, dz):
        """Zwróć nowy węzeł o początku w punktcie (x, y, z) i bokach dx, dy, dz"""
        self.x = x
        self.y = y
        self.z = z
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.is_leaf = True  # kazdy węzeł na początku jest liściem
        self.branches = [None] * 8

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
        return "({}, {}, {})\t -> {}, {}, {}".format(self.x, self.y, self.z, self.dx, self.dy, self.dz)

    def split(self):
        """Podziel węzeł na osiem"""
        self.is_leaf = False

        self.branches[0] = Node(
            self.x, 
            self.y, 
            self.z, 
            self.dx/2, 
            self.dy/2, 
            self.dz/2
        )

        self.branches[1] = Node(
            self.x + self.dx/2, 
            self.y, 
            self.z, 
            self.dx/2, 
            self.dy/2, 
            self.dz/2
        )

        self.branches[2] = Node(
            self.x, 
            self.y, 
            self.z + self.dz/2, 
            self.dx/2, 
            self.dy/2, 
            self.dz/2
        )

        self.branches[3] = Node(
            self.x + self.dx/2, 
            self.y, 
            self.z + self.dz/2, 
            self.dx/2, 
            self.dy/2, 
            self.dz/2
        )

        self.branches[4] = Node(
            self.x, 
            self.y + self.dy/2, 
            self.z, 
            self.dx/2, 
            self.dy/2, 
            self.dz/2
        )

        self.branches[5] = Node(
            self.x + self.dx/2, 
            self.y + self.dy/2, 
            self.z, 
            self.dx/2, 
            self.dy/2, 
            self.dz/2
        )

        self.branches[6] = Node(
            self.x, 
            self.y + self.dy/2, 
            self.z + self.dz/2, 
            self.dx/2, 
            self.dy/2, 
            self.dz/2
        )

        self.branches[7] = Node(
            self.x + self.dx/2, 
            self.y + self.dy/2, 
            self.z + self.dz/2, 
            self.dx/2, 
            self.dy/2, 
            self.dz/2
        )


class Octree:
    def __init__(self, dx, dy, dz):
        """Zwróć nowe drzewo o początku w punkcie (0,0,0) i wymiarach dz, dy, dz"""
        self.root = self.add_node(0, 0, 0, dx, dy, dz)

    def add_node(self, x, y, z, dx, dy, dz):
        """Zwróć nowy węzeł"""
        return Node(x, y, z, dz, dy, dz)


if __name__ == "__main__":
    oct = Octree(10, 10, 10)
    oct.root.split()
    for child in oct.root.branches:
        print(child)