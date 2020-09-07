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
        return f'({self.x}, {self.y}, {self.z}) -> {self.dx}, {self.dy}, {self.dz}'

    def can_be_split(self, condition):
        return self.dx > condition and self.dy > condition and self.dz > condition

    def split(self):
        """Podziel węzeł na osiem"""
        self.is_leaf = False

        dim = [self.dx / 2, self.dy / 2, self.dz / 2]

        self.branches[0] = Node([self.x, self.y, self.z], dim)
        self.branches[1] = Node([self.x + self.dx / 2, self.y, self.z], dim)
        self.branches[2] = Node([self.x, self.y, self.z + self.dz / 2], dim)
        self.branches[3] = Node([self.x + self.dx / 2, self.y, self.z + self.dz / 2], dim)
        self.branches[4] = Node([self.x, self.y + self.dy / 2, self.z], dim)
        self.branches[5] = Node([self.x + self.dx / 2, self.y + self.dy / 2, self.z], dim)
        self.branches[6] = Node([self.x, self.y + self.dy / 2, self.z + self.dz / 2], dim)
        self.branches[7] = Node([self.x + self.dx / 2, self.y + self.dy / 2, self.z + self.dz / 2], dim)
