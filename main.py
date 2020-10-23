import argparse

from models import Node, STL, Edge, Vertex
from functions import get_grid, print_preorder, show_model, my_show_model
from stl import mesh


def test_octree(dx, dy, dz):
    point = [0, 0, 0]
    dims = [1, 2, 4]  # 1*2*4 = 8

    print("TEST OCTREE")
    root = Node(point, dims)
    get_grid(root, condition=0.12)
    print_preorder(root)


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

    args = parser.parse_args()

    in_file = args.input
    # out_file = args.output
    dx = int(args.dx)
    dy = int(args.dy)
    dz = int(args.dz)

    # test_octree(dx, dy, dz)
    # print("-------------------------")
    # test_stl(in_file)
    stl = STL(in_file)
    my_show_model(stl)
