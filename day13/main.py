import os
from typing import Union
from enum import Enum

DATA_PATH = "E:\\gitcode\\adventofcode_2022\\day13\\data.txt"


class Comparison(Enum):
    RIGHT_ORDER = 0
    WRONG_ORDER = 1
    UNKNOWN = 2


def parse_data(data):
    packet_pairs = []

    eol = False
    idx = 0
    while not eol:
        p1 = eval(data[idx])
        p2 = eval(data[idx + 1])
        packet_pairs.append((p1, p2))
        idx += 3
        if idx > len(data):
            eol = True

    return packet_pairs

def _ws(depth):
    return "".join([" "] * depth * 2)


def check_order(p1: Union[list, int], p2: Union[list, int], depth: int=0):

    print(_ws(depth) + "- Compare", p1, "vs", p2)
    if isinstance(p1, int) and isinstance(p2, int):
        if p1 < p2:
            print(_ws(depth + 1) + "- Left side is smaller, so inputs are in the right order")
            return Comparison.RIGHT_ORDER
        elif p1 > p2:
            print(_ws(depth + 1) + "- Right side is smaller, so inputs are not in the right order")
            return Comparison.WRONG_ORDER
        else:
            return Comparison.UNKNOWN
    elif isinstance(p1, list) and isinstance(p2, int):
        print(_ws(depth + 1) + "- Mixed types; convert right to", str([p2]),"and retry comparison")
        return check_order(p1, [p2], depth + 1)
    elif isinstance(p1, int) and isinstance(p2, list):
        print(_ws(depth + 1) + "- Mixed types; convert left to", str([p1]),"and retry comparison")
        return check_order([p1], p2, depth + 1)
    elif isinstance(p1, list) and isinstance(p2, list):
        p1_size = len(p1)
        p2_size = len(p2)
        for i in range(min(p1_size, p2_size)):
            ret = check_order(p1[i], p2[i], depth + 1)
            if ret == Comparison.UNKNOWN:
                continue
            else:
                return ret
        if p1_size < p2_size:
            print(_ws(depth + 1) + "- Left side ran out of items, so inputs are in the right order")
            return Comparison.RIGHT_ORDER
        elif p2_size < p1_size:
            print(_ws(depth + 1) + "- Right side ran out of items, so inputs are not in the right order")
            return Comparison.WRONG_ORDER
        else:
            return Comparison.UNKNOWN
    else:
        print("SOMETHING WENT WRONG")
        import pdb; pdb.set_trace()


def main():
    with open(DATA_PATH) as file:
        data = [line.rstrip("\n") for line in file]

    packet_pairs = parse_data(data)
    checks = []
    for i, p in enumerate(packet_pairs):
        print("== Pair", i + 1, "==")
        comparison = check_order(p[0], p[1], 0)
        assert comparison != Comparison.UNKNOWN, "GOT UNKNOWN COMPARISON"
        checks.append(comparison)
        print()
    idxs = [i + 1 for i, b in enumerate(checks) if b == Comparison.RIGHT_ORDER]
    print("Sum indices:", sum(idxs))

    return 0 


if __name__ == "__main__":
    main()