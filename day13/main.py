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

    # print(_ws(depth) + "- Compare", p1, "vs", p2)
    if isinstance(p1, int) and isinstance(p2, int):
        if p1 < p2:
            # print(_ws(depth + 1) + "- Left side is smaller, so inputs are in the right order")
            return Comparison.RIGHT_ORDER
        elif p1 > p2:
            # print(_ws(depth + 1) + "- Right side is smaller, so inputs are not in the right order")
            return Comparison.WRONG_ORDER
        else:
            return Comparison.UNKNOWN
    elif isinstance(p1, list) and isinstance(p2, int):
        # print(_ws(depth + 1) + "- Mixed types; convert right to", str([p2]),"and retry comparison")
        return check_order(p1, [p2], depth + 1)
    elif isinstance(p1, int) and isinstance(p2, list):
        # print(_ws(depth + 1) + "- Mixed types; convert left to", str([p1]),"and retry comparison")
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
            # print(_ws(depth + 1) + "- Left side ran out of items, so inputs are in the right order")
            return Comparison.RIGHT_ORDER
        elif p2_size < p1_size:
            # print(_ws(depth + 1) + "- Right side ran out of items, so inputs are not in the right order")
            return Comparison.WRONG_ORDER
        else:
            return Comparison.UNKNOWN
    else:
        print("SOMETHING WENT WRONG")
        import pdb; pdb.set_trace()


def merge_packet_lists(l1, l2):
    result = []
    while len(l1) > 0 and len(l2) > 0:
        first_l1 = l1.pop(0)
        first_l2 = l2.pop(0)
        comparison = check_order(first_l1, first_l2)
        if comparison == Comparison.RIGHT_ORDER:
            result.append(first_l1)
            l2.insert(0, first_l2)
        elif comparison == Comparison.WRONG_ORDER:
            result.append(first_l2)
            l1.insert(0, first_l1)
        else:
            print("SOMETHING WENT WRONG")
            import pdb; pdb.set_trace()
        
    while len(l1) > 0:
        result.append(l1.pop(0))
    while len(l2) > 0:
        result.append(l2.pop(0))

    return result


def main():
    with open(DATA_PATH) as file:
        data = [line.rstrip("\n") for line in file]

    packet_pairs = parse_data(data)
    checks = []
    for i, p in enumerate(packet_pairs):
        # print("== Pair", i + 1, "==")
        comparison = check_order(p[0], p[1], 0)
        assert comparison != Comparison.UNKNOWN, "GOT UNKNOWN COMPARISON"
        checks.append(comparison)
        # print()
    idxs = [i + 1 for i, b in enumerate(checks) if b == Comparison.RIGHT_ORDER]
    print("Sum indices:", sum(idxs))

    packet_pairs_sorted = []
    for i, p in enumerate(packet_pairs):
        if checks[i] == Comparison.WRONG_ORDER:
            packet_pairs_sorted.append([p[1], p[0]])
        elif checks[i] == Comparison.RIGHT_ORDER:
            packet_pairs_sorted.append([p[0], p[1]])
        else:
            print("SOMETHING WENT WRONG")
            import pdb; pdb.set_trace()
    
    packet_pairs_sorted.append([[[2]], [[6]]])

    curr_list = packet_pairs_sorted.pop(0)
    while len(packet_pairs_sorted) > 0:
        next_item = packet_pairs_sorted.pop(0)
        curr_list = merge_packet_lists(curr_list, next_item)

    idxs_of_mrkrs = [i + 1 for i, x in enumerate(curr_list) if x == [[2]] or x == [[6]]]

    print("Decoder key:", idxs_of_mrkrs[0] * idxs_of_mrkrs[1])

    return 0 


if __name__ == "__main__":
    main()