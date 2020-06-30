class Node:
    def __init__(self, x, y, z, d):
        """Zwróć nowy węzeł o początku w punktcie (x, y, z) i boku d"""
        self.x = x
        self.y = y
        self.z = z
        self.d = d
        self.is_leaf = True  # kazdy węzeł na początku jest liściem
        self.branches = [None] * 8


if __name__ == "__main__":
    print([None]*8)