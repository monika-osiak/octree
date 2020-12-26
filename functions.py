import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np


def print_preorder(root, i=0, prefix="", last=True):
    if root:
        chars = {
            'mid': '├',
            'term': '└',
            'skip': '│',
            'dash': '─',
            'point': ' ' + str(root.percentage),
        }

        char = chars['term'] if last else chars['mid']
        new_prefix = (prefix + "    ") if last else (prefix + chars['skip'] + "   ")

        print(prefix + char + chars['dash'] * 2 + chars['point'])

        for i in range(8):
            status = True if i == 7 else False
            print_preorder(root.branches[i], i, new_prefix, status)


def get_grid(root, condition, object=None):
    if root:
        if root.can_be_split(condition, object):
            root.split()

            for child in root.branches:
                root.percentage += get_grid(child, condition, object) / 8
        else:
            root.determine_material(object)
            root.percentage = root.material
            return root.percentage
    return root.percentage


def get_array(root, array):
    if root:
        array = np.append(array, root.percentage)

        for child in root.branches:
            array = get_array(child, array)

    return array


def show_octree(root, stl=None):
    print('> Show the full octree...')
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    for p1, p2 in root.get_external_edges():
        draw_edge(p1, p2, ax)

    show_single_node(root, ax)

    if stl:
        print('> Show STL object...')
        for edge in tqdm(stl.edges):
            draw_edge(edge.a, edge.b, ax, 'red')

    plt.show()


def show_single_node(root, axes):
    if root and not root.is_leaf:
        for p1, p2 in root.get_inner_edges():
            draw_edge(p1, p2, axes)

        for child in root.branches:
            show_single_node(child, axes)


def show_object_octree(root, stl=None):
    print('> Show the octree with object nodes only...')
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    if stl:
        print('> Draw STL object...')
        for edge in tqdm(stl.edges):
            draw_edge(edge.a, edge.b, ax, 'red')

    for p1, p2 in root.get_external_edges():
        draw_edge(p1, p2, ax)

    show_object_single_node(root, ax)

    plt.show()


def show_object_single_node(root, axes):
    if root:
        if root.is_leaf and root.material == 1:
            for p1, p2 in root.get_external_edges():
                draw_edge(p1, p2, axes)

        for child in root.branches:
            show_object_single_node(child, axes)


def draw_edge(p1, p2, ax, color='gray'):
    xs = [p1.x, p2.x]
    ys = [p1.y, p2.y]
    zs = [p1.z, p2.z]
    ax.plot3D(xs, ys, zs, color)


def is_inside(triangles, X):
    # Compute triangle vertices and their norms relative to X
    M = triangles - X
    M_norm = np.sqrt(np.sum(M ** 2, axis=2))

    # Accumulate generalized winding number per triangle
    winding_number = 0.
    for (A, B, C), (a, b, c) in zip(M, M_norm):
        winding_number += np.arctan2(np.linalg.det(np.array([A, B, C])),
                                        (a * b * c) + c * np.dot(A, B) + a * np.dot(B, C) + b * np.dot(C, A))

    # Job done
    return winding_number >= 2. * np.pi
