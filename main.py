import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="File to read from")
    parser.add_argument("--output", help="File to save result")
    args = parser.parse_args()

    in_file = args.input
    out_file = args.output