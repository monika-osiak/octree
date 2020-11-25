import argparse
import configparser

from models import Node, STL, Point, Vector
from functions import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Configuration file")

    args = parser.parse_args()
    config_file = args.config

    config = configparser.ConfigParser()
    config.read(config_file)

    # TODO: add errors handling
    # TODO: move all to the new class

    start_point = Point(
        float(config['START POINT']['x']),
        float(config['START POINT']['y']),
        float(config['START POINT']['z']),
    )

    dimensions = Vector(
        float(config['SCENE DIMENSIONS']['dx']),
        float(config['SCENE DIMENSIONS']['dy']),
        float(config['SCENE DIMENSIONS']['dz']),
    )

    stl_file = config['OTHERS']['STL file path']
    condition = float(config['OTHERS']['minimum volume'])

    stl = STL(stl_file)
    root = Node(start_point, dimensions)
    get_grid(root, condition=condition, object=stl)
    print('> Show grid...')
    show_full_octree(root, stl)