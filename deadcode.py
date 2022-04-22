import sys
from parser import parse

if __name__ == '__main__':
    if len(sys.argv) != 1:
        print("Use of command:\n  python3 deadcode.py < ILOC file\n")
        exit(1)

    # parse instructions
    instructions = parse()

    for ixn in instructions:
        print(ixn)

