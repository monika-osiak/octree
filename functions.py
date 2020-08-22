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


def get_grid(root, condition):
    # TODO: split if there is edge from model in the node
    if root and root.can_be_split(condition):
        root.split()

        for child in root.branches:
            get_grid(child, condition)


def find_point(root, point):
    if root is None or root.is_leaf:
        return root
    else:
        x = point.x > root.vertex.x + root.get_dx() / 2
        y = point.y > root.vertex.y + root.get_dy() / 2
        z = point.z > root.vertex.z + root.get_dz() / 2
        i = x * 4 + y * 2 + z
        return find_point(root.branches[i], point)
