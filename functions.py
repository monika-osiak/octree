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


def show_model(filename):
    # Create a new plot
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)

    # Load the STL files and add the vectors to the plot
    your_mesh = mesh.Mesh.from_file(filename)
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))

    # Auto scale to the mesh size
    scale = your_mesh.points.flatten('F')
    axes.auto_scale_xyz(scale, scale, scale)

    # Show the plot to the screen
    pyplot.show()

# TODO: add function to plot octree in 3D


def draw_edge(edge, ax):
    xs = [edge.v1.x, edge.v2.x]
    ys = [edge.v1.y, edge.v2.y]
    zs = [edge.v1.z, edge.v2.z]
    ax.plot3D(xs, ys, zs, 'gray')


def my_show_model(stl):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    print(f'> Draw {stl.filename}...')
    for edge in tqdm(stl.e):
        draw_edge(edge, ax)
    plt.show()


def show_node(root, axes):
    if root:
        for edge in root.e:
            draw_edge(edge, axes)

        for child in root.branches:
            show_node(child, axes)


def show_octree(root):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    show_node(root, ax)
    plt.show()


def length(v):
    return sqrt(v.x ** 2 + v.y ** 2 + v.z ** 2)


def dot_product(v1, v2):
    return (-1) * (v1.x * v2.x + v1.y * v2.y + v1.z * v2.z)
