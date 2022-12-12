import copy
import os
import sys
from typing import Dict, List, Optional, Tuple
import heapq
import matplotlib.pyplot as plt


DATA_PATH = "E:\\gitcode\\adventofcode_2022\\day12\\data.txt"
############################
# Uses Djikstras Algorithm #
############################
class Grid:
    def __init__(self, grid_pos: Tuple[int, int]):
        self.grid_pos = grid_pos
        self.distance = float("inf")
        self.visited = False  
        self.previous = None
        self.adjacent = {}

    def add_neighbor_grid(self, neighbor: "Grid", weight=0):
        self.adjacent[neighbor] = weight

    def get_weight(self, neighbor: "Grid") -> int:
        return self.adjacent[neighbor]
    
    def __lt__(self, other: "Grid"):
        return self.distance < other.distance
    
    def __le__(self, other: "Grid"):
        return self.distance <= other.distance


class Map:
    def __init__(self) -> None:
        self.grid_dict = {}
        self.num_grids = 0
    
    def __iter__(self):
        return iter(self.grid_dict.values())
    
    def add_grid(self, grid_pos: Tuple[int, int]):
        self.num_grids += 1
        grid = Grid(grid_pos)
        self.grid_dict[grid_pos] = grid
        return grid
    
    def get_grid(self, grid_pos: Tuple[int, int]) -> Grid:
        return self.grid_dict[grid_pos] if grid_pos in self.grid_dict else None
    
    def add_connection(self, grid_pos_from: Tuple[int, int], grid_pos_to: Tuple[int, int], weight: int = 0):
        if grid_pos_from not in self.grid_dict:
            self.add_grid(grid_pos_from)
        if grid_pos_to not in self.grid_dict:
            self.add_grid(grid_pos_to)

        self.grid_dict[grid_pos_from].add_neighbor_grid(self.grid_dict[grid_pos_to], weight)



def run_dijkstra(heightmap: Map, start: Tuple[int, int], target: Tuple[int, int]):
    Q = [(v.distance, v) for v in heightmap]
    heapq.heapify(Q)

    while len(Q):
        u = heapq.heappop(Q)
        u = u[1]
        u.visited = True

        for v in u.adjacent:
            alt = u.distance + u.get_weight(v)
            
            if alt < v.distance:
                v.distance = alt
                v.previous = u
                print("Updated current =", u.grid_pos, ", next =", v.grid_pos, ", new_distance =", v.distance)
            else:
                print("Not Updated current =", u.grid_pos, ", next =", v.grid_pos, ", new_distance =", v.distance)

        # Rebuild Q
        while len(Q):
            heapq.heappop(Q)
        Q = [(v.distance, v) for v in heightmap if not v.visited]
        heapq.heapify(Q)


def build_map(data):
    heightmap = Map()
    h = len(data)
    w = len(data[0])

    start_pos = None
    end_pos = None

    # Add grids
    for j in range(h):
        for i in range(w):
            if data[j][i] == "S":
                start_pos = (i, j)
            elif data[j][i] == "E":
                end_pos = (i, j)
            heightmap.add_grid((i, j))
    
    # Add connections between grids
    for j in range(h):
        for i in range(w):
            h_curr = data[j][i]
            h_right = data[j][i + 1] if i + 1 < w else None
            h_down = data[j + 1][i] if j + 1 < h else None
            
            if h_curr == "S": h_curr = "a"
            if h_right == "S": h_right = "a"
            if h_down == "S": h_down = "a"
            if h_curr == "E": h_curr = "z"
            if h_right == "E": h_right = "z"
            if h_down == "E": h_down = "z"


            if h_right is not None:
                if abs(ord(h_right) - ord(h_curr)) <= 1:
                    heightmap.add_connection((i, j), (i + 1, j), 1)
                    heightmap.add_connection((i + 1, j), (i, j), 1)
                elif ord(h_right) < ord(h_curr):
                    heightmap.add_connection((i + 1, j), (i, j), 1)
                elif ord(h_curr) < ord(h_right):
                    heightmap.add_connection((i, j), (i + 1, j), 1)
            if h_down is not None:
                if abs(ord(h_down) - ord(h_curr)) <= 1:
                    heightmap.add_connection((i, j), (i, j + 1), 1)
                    heightmap.add_connection((i, j + 1), (i, j), 1)
                elif ord(h_down) < ord(h_curr):
                    heightmap.add_connection((i, j + 1), (i, j), 1)
                elif ord(h_curr) < ord(h_down):
                    heightmap.add_connection((i, j), (i, j + 1), 1)
    
    heightmap.get_grid(end_pos).distance = 0


    return heightmap, start_pos, end_pos


def shortest_path(heightmap: Map, grid_pos: Tuple[int, int]):
    path = [grid_pos]

    curr_pos = grid_pos

    while heightmap.get_grid(curr_pos).previous is not None:
        prev_pos = heightmap.get_grid(curr_pos).previous.grid_pos
        if prev_pos is None:
            break
        path.append(prev_pos)
        curr_pos = prev_pos
        

    return path


def main():
    with open(DATA_PATH) as file:
        data = [list(line.rstrip("\n")) for line in file]

    # plt.imshow([[ord(p) for p in r] for r in data], cmap='hot', interpolation='nearest')
    # plt.show()

    # Runs algorithm in reverse to get distance from any point to the end
    heightmap, start_pos, end_pos = build_map(data)
    run_dijkstra(heightmap, end_pos, start_pos)

    path = shortest_path(heightmap, start_pos)
    print("The shortest path:", path)
    print("Length path:", len(path) - 1)

    heatmap = copy.deepcopy(data)
    for g in heightmap:
        i, j = g.grid_pos
        heatmap[j][i] = g.distance
    
    plt.imshow(heatmap, cmap='hsv', interpolation='nearest')
    plt.show()

    a_dists = []
    for g in heightmap:
        if data[g.grid_pos[1]][g.grid_pos[0]] == "a":
            a_dists.append(g.distance)

    print("Min a dist:", min(a_dists))

    import pdb; pdb.set_trace()


    return 0


if __name__ == "__main__":
    main()