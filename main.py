import argparse

from models import Node, STL
from functions import get_grid, print_preorder, show_model
from stl import mesh

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="File to read from")

    # TODO: saving structure to file
    # parser.add_argument("--output", help="File to save result")

    parser.add_argument("--dx")
    parser.add_argument("--dy")
    parser.add_argument("--dz")

    args = parser.parse_args()

    in_file = args.input
    # out_file = args.output
    dx = int(args.dx)
    dy = int(args.dy)
    dz = int(args.dz)

    stl = STL(in_file)
    for triangle in stl.triangles:
        print(triangle)