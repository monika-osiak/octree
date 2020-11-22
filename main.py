import argparse

from models import Node, STL, Point, Vector
from functions import *


def test_octree(dx, dy, dz):
    point = Point(0, 0, 0)
    dims = Vector(1, 2, 4)  # 1*2*4 = 8

    print("TEST OCTREE")
    root = Node(point, dims)
    root.split()
    root.branches[2].split()
    get_grid(root, condition=0.12)
    show_octree(root)


def test_stl(in_file):
    stl = STL(in_file)

    print("TEST STL PARSER")
    print(f"Filename: {in_file}")
    print(f"Number of triangles: {len(stl.triangles)}")
    print(f"Number of vertices: {len(stl.vertices)}")
    print(f"Number of edges: {len(stl.edges)}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="File to read from")

    # TODO: saving structure to file
    # parser.add_argument("--output", help="File to save result")

    parser.add_argument("--dx")
    parser.add_argument("--dy")
    parser.add_argument("--dz")

    parser.add_argument("--condition")

    args = parser.parse_args()

    in_file = args.input
    # out_file = args.output
    dx = int(args.dx)
    dy = int(args.dy)
    dz = int(args.dz)
    condition = float(args.condition)

    # test_octree(dx, dy, dz)
    # print("-------------------------")
    # test_stl(in_file)
    stl = STL(in_file)
    root = Node(
        Point(0, 0, 0),
        Vector(dx, dy, dz)
    )
    get_grid(root, condition=condition, object=stl)
    print("> Show grid...")
    show_octree(root, stl)
