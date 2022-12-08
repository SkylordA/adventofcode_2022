import os
import numpy as np

DATA_PATH = "E:\\gitcode\\adventofcode_2022\\day08\\data.txt"


def check_if_visible(data, i, j):
    curr_tree_height = data[i][j]
    
    col = data[:, j]
    row = data[i, :]

    trees_north = col[:i]
    trees_south = col[i + 1:]
    trees_east = row[j + 1:]
    trees_west = row[:j]

    vis_north = all(trees_north < curr_tree_height) or len(trees_north) == 0
    vis_south = all(trees_south < curr_tree_height) or len(trees_south) == 0
    vis_east = all(trees_east < curr_tree_height) or len(trees_east) == 0
    vis_west = all(trees_west < curr_tree_height) or len(trees_west) == 0

    return any([vis_north, vis_south, vis_east, vis_west])


def get_scenic_score(data, i, j):
    curr_tree_height = data[i][j]
    
    col = data[:, j]
    row = data[i, :]

    trees_north = np.flip(col[:i])
    trees_south = col[i + 1:]
    trees_east = row[j + 1:]
    trees_west = np.flip(row[:j])

    count_up = 0
    for x in trees_north:
        if x < curr_tree_height: count_up += 1
        elif x >= curr_tree_height: 
            count_up += 1
            break
    
    count_dn = 0
    for x in trees_south:
        if x < curr_tree_height: count_dn += 1
        elif x >= curr_tree_height: 
            count_dn += 1
            break
    
    count_lf = 0
    for x in trees_west:
        if x < curr_tree_height: count_lf += 1
        elif x >= curr_tree_height: 
            count_lf += 1
            break

    count_rt = 0
    for x in trees_east:
        if x < curr_tree_height: count_rt += 1
        elif x >= curr_tree_height: 
            count_rt += 1
            break
    score = count_lf * count_dn * count_rt * count_up
    return score


def main():
    with open(DATA_PATH) as file:
        data = [line.rstrip("\n") for line in file]

    data = np.array(
        [
            np.array(list(map(int, list(x))))
            for x in data
        ]
    )

    is_visible = np.zeros(data.shape, dtype=bool)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            is_visible[i][j] = check_if_visible(data, i, j)
    print("NUM VISIBLE TREES:", np.sum(is_visible))

    scenic_scores = np.zeros(data.shape, dtype=int)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            scenic_scores[i][j] = get_scenic_score(data, i, j)
    print("MAX SCENIC SCORE:", np.max(scenic_scores))

    return 0 


if __name__ == "__main__":
    main()