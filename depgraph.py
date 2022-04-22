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
                print(f"Finding deps for leave: {leave}")
                reachable_nodes = self.get_deps(leave)
                for node in reachable_nodes:
                    print(f"\tFound reachable node from leave: {node.instruction}")
                    node.critical = True
                    new_leaves.append(node)
                

            leaves = new_leaves
            reached_fixed_point = len(leaves) == 0

    def get_deps(self, node: DepGraphNode) -> List[DepGraphNode]:
        deps = []

        op = node.instruction.opcode
        
        # ADD, SUB, MUL
        if op == OpCode.ADD or op == OpCode.SUB or op == OpCode.MUL:
            field_1_dep = self.get_register_deps(node.instruction, node.instruction.field1)
            field_2_dep = self.get_register_deps(node.instruction, node.instruction.field2)

            if field_1_dep == None or field_2_dep == None:
                print("get_deps: ADD,SUB,MUL cannot have None register deps!")
                exit(1)
            
            deps = [field_1_dep, field_2_dep]

        # OUTPUTAI
        elif op == OpCode.OUTPUTAI:
            field_1_dep = self.get_register_deps(node.instruction, node.instruction.field1)
            field_2_dep = self.get_memory_deps(node.instruction, node.instruction.field2)

            if field_1_dep == None or field_2_dep == None:
                print("get_deps: OUTPUTAI cannot have a None register or memory dep")
                exit(1)
            
            deps = [field_1_dep, field_2_dep]

        # LOADI
        elif op == OpCode.LOADI:
            # Can't have dependency on an immediate
            return []
        
        # STOREAI
        elif op == OpCode.STOREAI:
            field_1_dep = self.get_register_deps(node.instruction, node.instruction.field1)

            if field_1_dep == None:
                print("get_des: STOREAI cannot have a None field_1_dep")
                exit(1)

            deps = [field_1_dep]

        # LOADAI
        elif op == OpCode.LOADAI:
            field_1_dep = self.get_register_deps(node.instruction, node.instruction.field1)
            field_2_dep = self.get_memory_deps(node.instruction, node.instruction.field2)

            if field_1_dep == None:
                print("get_deps: LOADAI cannot have a None field_1_dep")
                exit(1)

            if field_2_dep == None:
                deps = [field_1_dep]
            else:
                deps = [field_1_dep, field_2_dep]

        else:
            print(f"get_deps: OpCode {op} not yet implemented")
            exit(1)
        
        return [self.get_or_insert_node(x) for x in deps]


    def get_register_deps(self, instruction: Instruction, register: int) -> Optional[Instruction]:
        previous_ixns = self.get_previous_instructions(instruction)
        if previous_ixns == None:
            return None

        for ixn in previous_ixns:
            # LOADI
            if ixn.opcode == OpCode.LOADI:
                if ixn.field2 == register:
                    return ixn
            
            # ADD, SUB, MUL, LOADAI
            elif ixn.opcode == OpCode.ADD or \
                 ixn.opcode == OpCode.SUB or \
                 ixn.opcode == OpCode.MUL or \
                 ixn.opcode == OpCode.LOADAI:
                     if ixn.field3 == register:
                         return ixn
            # STOREAI
            elif ixn.opcode == OpCode.STOREAI:
                # SKIP 
                continue

            # OUTPUTAI
            elif ixn.opcode == OpCode.OUTPUTAI:
                # SKIP
                continue
            
            else:
                print(f"find_regsiter_deps: opcode {ixn.opcode} not yet implemented")
                exit(1)

    def get_memory_deps(self, instruction: Instruction, address: int) -> Optional[Instruction]:
        previous_ixns = self.get_previous_instructions(instruction)     
        if previous_ixns == None:
            return None

        for ixn in previous_ixns:
            # STOREAI
            if ixn.opcode == OpCode.STOREAI:
                if ixn.field3 == address:
                    return ixn

            # LOADAI
            elif ixn.opcode == OpCode.LOADAI:
                if ixn.field2 == address:
                    return ixn
            
            # ADD, SUB, MUL, LOADI, OUTPUTAI
            elif ixn.opcode == OpCode.ADD or ixn.opcode == OpCode.SUB or \
                 ixn.opcode == OpCode.MUL or ixn.opcode == OpCode.LOADI or \
                 ixn.opcode == OpCode.LOADI or ixn.opcode == OpCode.OUTPUTAI:
                     # SKIP
                     continue
            else:
                print(f"get_memory_deps: opcode {ixn.opcode} not yet implemented")
                exit(1)

    def get_previous_instructions(self, instruction: Instruction) -> Optional[List[Instruction]]:
        try:
            reversedIxns = self.instructions[::-1]
            return reversedIxns[reversedIxns.index(instruction) + 1 ::]
        except:
            return None
