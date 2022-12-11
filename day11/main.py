import os
from tqdm import tqdm
import operator
import numpy as np
from typing import Dict, List, Optional
import math

DATA_PATH = "E:\\gitcode\\adventofcode_2022\\day11\\data.txt"


class Monkey:
    def __init__(
            self,
            monkey_id: int,
            start_items:List[int],
            operator: str,
            operation_num: Optional[int],
            div_test_num: int,
            monk_div_true: int,
            monk_div_false: int,
            worry_decrease: bool=True,
            lcm: Optional[int]=None
        ):
        self.id = monkey_id
        self.items = start_items
        self.operator = operator
        self.operation_num = operation_num
        self.div_test_num = div_test_num
        self.monk_div_true = monk_div_true
        self.monk_div_false = monk_div_false
        self.num_inspections = 0
        self.worry_decrease = worry_decrease
        self.lcm = lcm
        ops = ["+","*"]
        if operator not in ops:
            assert False, "OP NOT FOUND" + operator

    def process_turn(self) -> Dict[int, List[int]]:
        # Returns which monkey gets which items
        pass_to_monkeys = {
            self.monk_div_true: [],
            self.monk_div_false: []
        }
        for i in self.items:
            if self.operation_num is None:
                if self.operator == "+":
                    i += i
                elif self.operator == "*":
                    i *= i
            else:
                if self.operator == "+":
                    i += self.operation_num
                elif self.operator == "*":
                    i *= self.operation_num
            if self.worry_decrease:
                i = int(i / 3)
            if self.lcm is not None:
                i = operator.mod(i, self.lcm)
            if i % self.div_test_num == 0:
                pass_to_monkeys[self.monk_div_true].append(i)
            else:
                pass_to_monkeys[self.monk_div_false].append(i)
        self.num_inspections += len(self.items)
        self.items = []
        return pass_to_monkeys


class MonkeyManager:
    def __init__(
            self, data: List[str],
            worry_decrease: bool=True,
        ):
        self.worry_decrease = worry_decrease
        self.lcm = None
        self.monkeys = self._generate_initial_monkeys(data)


    def _make_a_monkey(self, monkey_data):
        monkey_id = int(monkey_data[0].split(" ")[1].replace(":", ""))
        
        items_str = monkey_data[1].replace("Starting items: ", "").lstrip()
        items = [int(s) for s in items_str.split(',')]

        op_str = monkey_data[2].replace("Operation: new = old ", "").lstrip()
        operator = op_str[0]
        op_val_str = op_str.split(" ")[1]
        if op_val_str == "old":
            operation_num = None
        else:
            operation_num = int(op_str.split(" ")[1])

        div_test_num = int(monkey_data[3].split(" ")[-1])
        monk_div_true = int(monkey_data[4].split(" ")[-1])
        monk_div_false = int(monkey_data[5].split(" ")[-1])

        worry_decrease = self.worry_decrease

        return Monkey(
            monkey_id=monkey_id,
            start_items=items,
            operator=operator,
            operation_num=operation_num,
            div_test_num=div_test_num,
            monk_div_true=monk_div_true,
            monk_div_false=monk_div_false,
            worry_decrease=worry_decrease
        )


    def _generate_initial_monkeys(self, data: List[str]):
        monkeys = []
        i = 0
        eol = False
        while not eol:
            monkeys.append(self._make_a_monkey(data[i:i+6]))
            i += 7
            if i >= len(data):
                eol = True
        lcm = 1
        for m in monkeys:
            lcm = lcm*m.div_test_num//math.gcd(lcm, m.div_test_num)
        self.lcm = lcm

        for m in monkeys:
            m.lcm = lcm

        return monkeys
    
    def get_monkey_business(self) -> int:
        inspections = [m.num_inspections for m in self.monkeys]
        inspections = sorted(inspections, reverse=True)
        return inspections[0] * inspections[1]


    def simulate_rounds(self, num_rounds: int):
        for i in tqdm(range(num_rounds)):
            # print("BEFORE ROUND", i + 1)
            # for m in self.monkeys:
            #     print("Monkey", str(m.id) + ":", m.items)
            for m in self.monkeys:
                pass_monkey_dict = m.process_turn()
                for mid in pass_monkey_dict.keys():
                    self.monkeys[mid].items.extend(pass_monkey_dict[mid])
        
        print("### FINISHED ###")
        # for m in self.monkeys:
        #     print("Monkey", str(m.id) + ":", m.items)


def main():
    with open(DATA_PATH) as file:
        data = [line.rstrip("\n") for line in file]

    manager = MonkeyManager(data)
    manager.simulate_rounds(20)
    mb = manager.get_monkey_business()
    print("Monkey Business:", mb)

    manager2 = MonkeyManager(data, worry_decrease=False)
    manager2.simulate_rounds(10000)
    mb2 = manager2.get_monkey_business()
    print("Monkey Business2:", mb2)

    return 0 


if __name__ == "__main__":
    main()