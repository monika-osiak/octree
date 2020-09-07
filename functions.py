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
        x = point[0] > root.x + root.dx / 2
        y = point[1] > root.y + root.dy / 2
        z = point[2] > root.z + root.dz / 2
        i = x * 4 + y * 2 + z
        return find_point(root.branches[i], point)
