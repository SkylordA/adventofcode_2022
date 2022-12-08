import os

DATA_PATH = "E:\\gitcode\\adventofcode_2022\\day02\\data.txt"

OPP_CHOICE = ["A", "B", "C"]

PLR_CHOICE = ["X", "Y", "Z"]

def generate_all_pts_comb():
    # Assuming PLR_CHOICE is the move to play
    all_pts_comb = {}

    for c in OPP_CHOICE:
        all_pts_comb[c] = {}
    for i, c in enumerate(all_pts_comb.keys()):
        for j, d in enumerate(PLR_CHOICE):
            choice_point = j + 1
            if i == j:
                match_point = 3
            elif j == i + 1 or (j == 0 and i == 2):
                match_point = 6
            elif i == j + 1 or (j == 2 and i == 0):
                match_point = 0
            else:
                assert False, "ERROR, SOMETHING WENT WRONG"
            all_pts_comb[c][d] = choice_point + match_point

    return all_pts_comb

def generate_all_pts_comb_2():
    # Assuming PLR_CHOICE is desired outcome
    all_pts_comb = {}

    for c in OPP_CHOICE:
        all_pts_comb[c] = {}
    for i, c in enumerate(all_pts_comb.keys()):
        for j, d in enumerate(PLR_CHOICE):
            if d == "X":
                match_point = 0
                choice_point = ((i - 1) % 3) + 1
            if d == "Y":
                match_point = 3
                choice_point = i + 1
            if d == "Z":
                match_point = 6
                choice_point = ((i + 1) % 3) + 1
            all_pts_comb[c][d] = choice_point + match_point

    return all_pts_comb


def main():
    with open(DATA_PATH) as file:
        data = [line.rstrip().split(" ") for line in file]

    all_pts_comb = generate_all_pts_comb()
    print("All points comb dict:", all_pts_comb)
    points = [all_pts_comb[d[0]][d[1]] for d in data]
    print("Total points:", sum(points))

    all_pts_comb_2 = generate_all_pts_comb_2()
    print("All points comb dict 2:", all_pts_comb_2)
    points = [all_pts_comb_2[d[0]][d[1]] for d in data]
    print("Total points:", sum(points))


    return 0


if __name__ == "__main__":
    main()