import sys
from parser import parse
from depgraph import DepGraph

if __name__ == '__main__':
    if len(sys.argv) != 1:
        print("Use of command:\n  python3 deadcode.py < ILOC file\n")
        exit(1)

    # parse instructions
    instructions = parse()

    # Build graph
    graph = DepGraph(instructions)

    # Perform optimization pass
    graph.mark_reachable_code()

    for ixn in instructions:
        print(ixn)

