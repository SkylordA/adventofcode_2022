import os
from typing import List

DATA_PATH = "E:\\gitcode\\adventofcode_2022\\day05\\data.txt"

class Stacks:
    def __init__(self, init_stack_str_state: List[str]):
        self.init_stack_str_state = init_stack_str_state
        self._populate_stack_lists()

    def _populate_stack_lists(self):
        stack_names = self.init_stack_str_state[-1].split()

        stacks = []
        for n in stack_names:
            stacks.append([])
        
        for i in range(0, len(self.init_stack_str_state) - 1):
            crates = self._parse_crate_line(self.init_stack_str_state[i])
            assert len(crates) == len(stack_names), "STACK AND CRATE NUMBER MISMATCH"
            for j, c in enumerate(crates):
                if c != "":
                    stacks[j].insert(0, c)
        
        self.stacks = stacks
        self.stack_names = stack_names
        print("### INIT STACK STATE ###")
        self.print_stack()
        print("########################")
    
    def _parse_crate_line(self, crate_line_str):
        crate_list = []

        # Removes spaces between crates
        crate_line_str = "".join([c for i, c in enumerate(crate_line_str) if (i + 1) % 4 != 0])
        # Takes crate content at each stack
        crate_line_str = "".join([c for i, c in enumerate(crate_line_str) if (i - 1) % 3 == 0])

        for c in crate_line_str:
            crate_list.append(c.replace(" ", ""))

        return crate_list 

    def print_stack(self):
        stacks_str = ""

        first = True
        for n in self.stack_names:
            if not first:
                stacks_str += " "
            else:
                first = False
            stacks_str += " " + str(n) + " "
        
        stacks_max_height = max([len(s) for s in self.stacks])

        for i in range(stacks_max_height):
            first = True
            curr_stack_str = ""
            
            for stack in self.stacks:
                if not first:
                    curr_stack_str += " "
                else:
                    first = False
                try:
                    c = "[" + stack[i] + "]"
                except IndexError as e:
                    c = "   "
                curr_stack_str += c
            
            stacks_str = curr_stack_str + "\n" + stacks_str
        
        print(stacks_str)
    
    def print_top_crates(self):
        top_crate_str = ""

        for s in self.stacks:
            top_crate_str += s[-1]
        print("TOP CRATE STRING:", top_crate_str)

    def move_9000(self, amount: int, from_stack: str, to_stack: str):
        from_stack_idx = self.stack_names.index(from_stack)
        to_stack_idx = self.stack_names.index(to_stack)
        
        for _ in range(amount):
            crate = self.stacks[from_stack_idx].pop()
            self.stacks[to_stack_idx].append(crate)
    
    def move_9001(self, amount: int, from_stack: str, to_stack: str):
        from_stack_idx = self.stack_names.index(from_stack)
        to_stack_idx = self.stack_names.index(to_stack)
        
        idx = len(self.stacks[from_stack_idx]) - (amount)
        for _ in range(amount):
            crate = self.stacks[from_stack_idx].pop(idx)
            self.stacks[to_stack_idx].append(crate)


def clean_and_split_data(data):
    data_clean = [x for x in data if x != ""]

    instr_idx = None
    for i, x in enumerate(data):
        if "move" in x:
            instr_idx = i - 1
            break
    
    return data_clean[:instr_idx], data_clean[instr_idx:]

def get_instruction_params(inst_str):
    instr_list = inst_str.split(" ")
    amount = int(instr_list[1])
    from_stack = instr_list[3]
    to_stack = instr_list[5]
    return amount, from_stack, to_stack

def main():
    with open(DATA_PATH) as file:
        data = [line.rstrip("\n") for line in file]
    
    stack_str_list, instructions_list = clean_and_split_data(data)

    stack = Stacks(stack_str_list)

    [stack.move_9000(*get_instruction_params(i)) for i in instructions_list]

    stack.print_stack()
    stack.print_top_crates()

    stack2 = Stacks(stack_str_list)

    [stack2.move_9001(*get_instruction_params(i)) for i in instructions_list]
    stack2.print_stack()
    stack2.print_top_crates()


    return 0


if __name__ == "__main__":
    main()