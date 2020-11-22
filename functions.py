import matplotlib.pyplot as plt
from tqdm import tqdm


def get_grid(root, condition, object=None):
    if root and root.can_be_split(condition, object):
        root.split()

        for child in root.branches:
            get_grid(child, condition, object)


def show_octree(root, stl=None):
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    for p1, p2 in root.get_external_edges():
        draw_edge(p1, p2, ax)

    show_single_node(root, ax)

    if stl:
        print('> Draw STL object...')
        for edge in tqdm(stl.edges):
            draw_edge(edge.a, edge.b, ax, 'red')

    plt.show()


def show_single_node(root, axes):
    if root and not root.is_leaf:
        for p1, p2 in root.get_inner_edges():
            draw_edge(p1, p2, axes)

        for child in root.branches:
            show_single_node(child, axes)


def draw_edge(p1, p2, ax, color='gray'):
    xs = [p1.x, p2.x]
    ys = [p1.y, p2.y]
    zs = [p1.z, p2.z]
    ax.plot3D(xs, ys, zs, color)
