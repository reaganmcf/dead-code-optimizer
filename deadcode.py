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

    # remove dead instructions
    optimized_ixns = []
    for node in graph.nodes.values():
        if node.critical:
            optimized_ixns.append(node.instruction)

    for ixn in optimized_ixns:
        print(ixn.iloc_str())

    #percentage_removed = (len(instructions) - len(optimized_ixns)) / len(instructions)
    #print(f"Original: {len(instructions)} vs Optimized: {len(optimized_ixns)}", file = sys.stderr)

