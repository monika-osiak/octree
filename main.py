import argparse

from models import Node, Scene, Point
from functions import get_grid, print_preorder, find_point

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # TODO: Reading from STL file
    # parser.add_argument("--input", help="File to read from")

    # TODO: saving structure to file
    # parser.add_argument("--output", help="File to save result")

    parser.add_argument("--dx")
    parser.add_argument("--dy")
    parser.add_argument("--dz")

    args = parser.parse_args()

    # in_file = args.input
    # out_file = args.output
    dx = int(args.dx)
    dy = int(args.dy)
    dz = int(args.dz)

    # debug only
    scene = Scene(dx, dy, dz)
    octree = Node(scene, 0, 0, 0)
    get_grid(octree, 3)
    print_preorder(octree)
    print()
    p = Point(7, 7, 7)
    node = find_point(octree, p)
    print(f'Punkt {p} znajduje się w punkcie o danych {node}')