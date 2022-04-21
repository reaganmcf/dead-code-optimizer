from enum import Enum
class OpCode(Enum):
    LOADI = 0
    LOADAI = 1
    STOREAI = 2
    ADD = 3
    SUB = 4
    MUL = 5
    OUTPUTAI = 6

class Instruction:
    def __init__(self, id: int, opcode: OpCode, field1: int, field2: int, field3: int):
        self.id = id
        self.opcode = opcode
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3

    def __str__(self):
        return f"(id={self.id}) {self.iloc_str()}"
        
    def iloc_str(self):
        if (self.opcode == OpCode.LOADI):
            return f"loadI {self.field1} => r{self.field2}"
        elif (self.opcode == OpCode.LOADAI):
            return f"loadAI r{self.field1}, {self.field2} => r{self.field3}"
        elif (self.opcode == OpCode.STOREAI):
            return f"storeAI r{self.field1} => r{self.field2}, {self.field3}"
        elif (self.opcode == OpCode.ADD):
            return f"add r{self.field1}, r{self.field2} => r{self.field3}"
        elif (self.opcode == OpCode.SUB):
            return f"sub r{self.field1}, r{self.field2} => r{self.field3}"
        elif (self.opcode == OpCode.MUL):
            return f"mult r{self.field1}, r{self.field2} => r{self.field3}"
        else:
            return f"outputAI r{self.field1}, {self.field2}"

