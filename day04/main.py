import os

DATA_PATH = "E:\\gitcode\\adventofcode_2022\\day04\\data.txt"

def conver_to_ints(range_str):
    range_data = range_str.split("-")
    return [int(range_data[0]), int(range_data[1])]

def _check_overlap(val, elf_range):
    return elf_range[0] <= val and val <= elf_range[1]

def check_overlaps(elf1_range, elf2_range):
    overlap_conds = []
    overlap_conds.append(
        _check_overlap(elf1_range[0], elf2_range)
    )
    overlap_conds.append(
        _check_overlap(elf1_range[1], elf2_range)
    )
    overlap_conds.append(
        _check_overlap(elf2_range[0], elf1_range)
    )
    overlap_conds.append(
        _check_overlap(elf2_range[1], elf1_range)
    )

    return any(overlap_conds)


def check_overlaps_fully(elf1_range, elf2_range):
    # E1: ..345-
    # E2: .2345-
    if elf1_range[0] >= elf2_range[0]:
        # E1: -67...
        # E2: -678..
        if elf2_range[1] >= elf1_range[1]:
            return True
    
    # vice versa
    if elf2_range[0] >= elf1_range[0]:
        if elf1_range[1] >= elf2_range[1]:
            return True

    return False

def main():
    with open(DATA_PATH) as file:
        data = [line.rstrip().split(",") for line in file]

    fully_overlaps = [
        check_overlaps_fully(
            conver_to_ints(d[0]),
            conver_to_ints(d[1])
        ) for d in data
    ]

    print("Num fully overlapping pairs:", sum(fully_overlaps))
    
    overlaps = [
        check_overlaps(
            conver_to_ints(d[0]),
            conver_to_ints(d[1])
        ) for d in data
    ]
    print("Num overlapping pairs:", sum(overlaps))

    return 0


if __name__ == "__main__":
    main()