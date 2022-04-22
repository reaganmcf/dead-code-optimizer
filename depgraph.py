import sys
from typing import *
from instruction import *

class DepGraphNode:
    def __init__(self, instruction):
        self.id = instruction.id
        self.instruction = instruction
        self.deps = []
        self.critical = False

    def __str__(self):
        return str(self.instruction)

class DepGraph:
    def __init__(self, instructions: List[Instruction]):
        self.nodes = {}
        self.instructions = instructions

        # Start off by making all OUTPUTAI nodes critical
        for ixn in instructions:
            node = self.get_or_insert_node(ixn)
            if ixn.opcode == OpCode.OUTPUTAI:
                node.critical = True
        
    def get_or_insert_node(self, instruction: Instruction) -> DepGraphNode:
        try:
            v = self.nodes[str(instruction.id)]
            return v
        except:
            self.nodes[str(instruction.id)] = DepGraphNode(instruction)
            return self.nodes[str(instruction.id)]
    
    def mark_reachable_code(self):
        # do optimization pass
        
        reached_fixed_point = False

        # Anything that depends on OUTPUTAI is deemed critical
        leaves = [node for node in self.nodes.values() if node.critical]

        while not reached_fixed_point:
            new_leaves = []
            for leave in leaves:
                reachable_nodes = self.get_deps(leave)
                print(f"Finding deps for leave: {leave}")

            leaves = new_leaves
            reached_fixed_point = len(leaves) == 0

    def get_deps(self, node: DepGraphNode) -> List[DepGraphNode]:
        print('get deps nyi')
