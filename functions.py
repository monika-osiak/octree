from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
import matplotlib.pyplot as plt
from tqdm import tqdm
from math import sqrt


def print_preorder(root, i=0, prefix="", last=True):
    chars = {
        'mid': '├',
        'term': '└',
        'skip': '│',
        'dash': '─',
        'point': ' ' + str(i),
    }

    if root:
        char = chars['term'] if last else chars['mid']
        new_prefix = (prefix + "    ") if last else (prefix + chars['skip'] + "   ")

        print(prefix + char + chars['dash'] * 2 + chars['point'])

        for i in range(8):
            status = True if i == 7 else False
            print_preorder(root.branches[i], i, new_prefix, status)


def get_grid(root, condition, object=None):
    if root and root.can_be_split(condition, object):
        root.split()

        for child in root.branches:
            get_grid(child, condition, object)


def show_octree(root, stl=None):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    edges = [
        [root.vertices[0], root.vertices[1]],
        [root.vertices[1], root.vertices[3]],
        [root.vertices[3], root.vertices[2]],
        [root.vertices[2], root.vertices[0]],
        [root.vertices[0], root.vertices[4]],
        [root.vertices[1], root.vertices[5]],
        [root.vertices[3], root.vertices[7]],
        [root.vertices[2], root.vertices[6]],
        [root.vertices[4], root.vertices[5]],
        [root.vertices[5], root.vertices[7]],
        [root.vertices[7], root.vertices[6]],
        [root.vertices[6], root.vertices[4]],
    ]
    for p1, p2 in edges:
        draw_edge_from_points(p1, p2, ax)
    show_node(root, ax)
    if stl:
        print('> Draw STL object...')
        for edge in tqdm(stl.edges):
            draw_edge(edge, ax, 'red')
    plt.show()


def show_node(root, axes):
    if root and not root.is_leaf:
        for p1, p2 in root.middle_edges:
            draw_edge_from_points(p1, p2, axes)

        for child in root.branches:
            show_node(child, axes)


def draw_edge(edge, ax, color='gray'):
    xs = [edge.a.x, edge.b.x]
    ys = [edge.a.y, edge.b.y]
    zs = [edge.a.z, edge.b.z]
    ax.plot3D(xs, ys, zs, color)


def draw_edge_from_points(p1, p2, ax, color='gray'):
    xs = [p1.x, p2.x]
    ys = [p1.y, p2.y]
    zs = [p1.z, p2.z]
    ax.plot3D(xs, ys, zs, color)


def show_model(stl):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    print(f'> Draw {stl.filename}...')
    for edge in tqdm(stl.e):
        draw_edge(edge, ax)
    plt.show()


def length(v):
    return sqrt(v.x ** 2 + v.y ** 2 + v.z ** 2)


def dot_product(v1, v2):
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z
