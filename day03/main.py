import os
import string

DATA_PATH = "E:\\gitcode\\adventofcode_2022\\day03\\data.txt"
ITEM_PRIORITY_ORDER = list(string.ascii_lowercase) + list(string.ascii_uppercase)

def find_common_items(items):
    n_items = len(items)
    assert n_items % 2 == 0, "ODD NUMBER OF ITEMS, WHAT DO?"

    comp1, comp2 = items[:n_items // 2], items[n_items // 2:]
    common = list(set(comp1).intersection(comp2))
    assert len(common) == 1, "MORE THAN ONE COMMON ITEM"

    return common[0]

def find_common_item_in_group(group_items):
    assert len(group_items) == 3, "NOT EQUAL TO 3 ITEM SETS IN GROUP"

    common = set(group_items[0])
    for items in group_items[1:]:
        common.intersection_update(items)

    assert len(common) == 1, "MORE THAN ONE COMMON ITEM"

    return list(common)[0]

def main():
    with open(DATA_PATH) as file:
        data = [line.rstrip() for line in file]
    
    commons = [find_common_items(item) for item in data]
    priorities = [ITEM_PRIORITY_ORDER.index(c) + 1 for c in commons]
    print("Sum priorities of common items per bag", sum(priorities))
    
    group_size = 3
    data_grouped = zip(*(iter(data),) * group_size)
    commons = [find_common_item_in_group(item) for item in data_grouped]
    priorities = [ITEM_PRIORITY_ORDER.index(c) + 1 for c in commons]
    print("Sum priorities of common items per group", sum(priorities))
    
    return 0


if __name__ == "__main__":
    main()