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
