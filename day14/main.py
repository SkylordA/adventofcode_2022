import os
from typing import List, Tuple
import numpy as np

DATA_PATH = "E:\\gitcode\\adventofcode_2022\\day14\\data.txt"


class Cave:
    def __init__(self, sand_start_pos: Tuple[int, int]):
        self.sand_start_pos = sand_start_pos
        self.rock_coords = []
        self.sand_coords = []
        
        self.cave_minx = sand_start_pos[0]
        self.cave_maxx = sand_start_pos[0]
        self.cave_miny = sand_start_pos[1]
        self.cave_maxy = sand_start_pos[1]

    def set_rocks(self, data):
        rock_draw_instrs = []
        for l in data:
            line_contents = l.split(" ")
            
            prev_coord = None
            for i in line_contents:
                if i == "->":
                    continue
                else:
                    curr_coord = eval("(" + i + ")")
                    if prev_coord is None:
                        prev_coord = curr_coord
                    else:
                        rock_draw_instrs.append((prev_coord, curr_coord))
                        prev_coord = curr_coord

        for p1, p2 in rock_draw_instrs:
            minx = min(p1[0], p2[0])
            maxx = max(p1[0], p2[0])
            miny = min(p1[1], p2[1])
            maxy = max(p1[1], p2[1])

            self.cave_minx = min(self.cave_minx, minx)
            self.cave_maxx = max(self.cave_maxx, maxx)
            self.cave_miny = min(self.cave_miny, miny)
            self.cave_maxy = max(self.cave_maxy, maxy)
            for x in range(minx, maxx + 1):
                for y in range(miny, maxy + 1):
                    self.rock_coords.append((x, y))
        
        self.rock_coords = list(set(self.rock_coords))
    

    def print_cave(self):
        encoding = "utf-8"
        charar_rangex = self.cave_maxx - self.cave_minx + 4
        charar_rangey = self.cave_maxy - self.cave_miny + 4
        charar = np.chararray((charar_rangey, charar_rangex), unicode=True)
        charar[:] = "/"

        yrange_strs = ["%03d" % y for y in range(self.cave_miny, self.cave_maxy + 1)]
        xrange_strs = ["%03d" % x for x in range(self.cave_minx, self.cave_maxx + 1)]


        # Set y axis
        for j, s in enumerate(charar):
            if j < 3:
                continue
            for i, c in enumerate(s):
                if i >= 3:
                    continue
                else:
                    charar[j][i] = yrange_strs[j - 3][i]

        # Set x axis
        for j, s in enumerate(charar):
            if j >= 3:
                continue
            for i, c in enumerate(s):
                if i < 3:
                    continue
                else:
                    charar[j][i] = xrange_strs[i - 3][j]

        # Set Air
        for j, s in enumerate(charar):
            if j < 3:
                continue
            for i, c in enumerate(s):
                if i < 3:
                    continue
                else:
                    charar[j][i] = "."

        # Set Rocks
        for x, y in self.rock_coords:
            j = y - self.cave_miny + 3
            i = x - self.cave_minx + 3
            charar[j][i] = "#"
        
        # Set Sand
        for x, y in self.sand_coords:
            j = y - self.cave_miny + 3
            i = x - self.cave_minx + 3
            charar[j][i] = "o"
        
        # Set Sand Start
        sand_x = self.sand_start_pos[0] - self.cave_minx + 3
        sand_y = self.sand_start_pos[1] - self.cave_miny + 3
        charar[sand_y][sand_x] = "+"

        # Print Cave
        for s in charar:
            string = ""
            for c in s:
                string += c
            print(string)

    def pos_within_bounds(self, pos: Tuple[int, int]):
        x, y = pos[0], pos[1]
        return ((x >= self.cave_minx and x <= self.cave_maxx) and
                (y >= self.cave_miny and y <= self.cave_maxy))

    def next_sand_pos(self, curr_sand_pos: Tuple[int, int]):
        sx, sy = (curr_sand_pos[0], curr_sand_pos[1])
        if ((sx, sy + 1) not in self.rock_coords and 
            (sx, sy + 1) not in self.sand_coords):
            new_pos = (sx, sy + 1)
            return self.pos_within_bounds(new_pos), new_pos
        elif ((sx - 1, sy + 1) not in self.rock_coords and 
            (sx - 1, sy + 1) not in self.sand_coords):
            new_pos = (sx - 1, sy + 1)
            return self.pos_within_bounds(new_pos), new_pos
        elif ((sx + 1, sy + 1) not in self.rock_coords and 
            (sx + 1, sy + 1) not in self.sand_coords):
            new_pos = (sx + 1, sy + 1)
            return self.pos_within_bounds(new_pos), new_pos
        else:
            return False, (sx, sy)

    def simulate_sand_void(self):
        in_void = False
        while not in_void:
            curr_sand_pos = self.sand_start_pos
            sand_can_move = True
            while sand_can_move:
                sand_can_move, curr_sand_pos = self.next_sand_pos(curr_sand_pos)
            
            if self.pos_within_bounds(curr_sand_pos):
                self.sand_coords.append(curr_sand_pos)
                # self.print_cave()
                # import time; time.sleep(1)
            else:
                in_void = True

        print("Num sand units:", len(self.sand_coords))
        print("Done!")

    
    def simulate_sand_floor(self):
        num_sand = 0
        is_full = False
        while not is_full:
            curr_sand_pos = self.sand_start_pos
            sand_can_move = True
            while sand_can_move:
                sand_can_move, curr_sand_pos = self.next_sand_pos(curr_sand_pos)                    
                
                if not self.pos_within_bounds(curr_sand_pos):
                    sand_can_move = True
                    self.cave_minx = min(self.cave_minx, curr_sand_pos[0])
                    self.cave_maxx = max(self.cave_maxx, curr_sand_pos[0])
                
                if curr_sand_pos[1] + 1 == self.cave_maxy:
                    sand_can_move = False
                    new_floor_rock = (curr_sand_pos[0], curr_sand_pos[1] + 1)
                    self.rock_coords.append(new_floor_rock)
            
            if curr_sand_pos == self.sand_start_pos:
                is_full = True
            else: 
                self.sand_coords.append(curr_sand_pos)
                num_sand += 1
                print(num_sand)
                # self.print_cave()
                # import time; time.sleep(0.05)

        print("Num sand units:", len(self.sand_coords) + 1)
        print("Done!")

def main():
    with open(DATA_PATH) as file:
        data = [line.rstrip("\n") for line in file]

    cave = Cave((500,0))
    
    # Part 1
    cave.set_rocks(data)
    # cave.print_cave()
    # cave.simulate_sand_void()
    # cave.print_cave()

    # Part 2
    floor_level = cave.cave_maxy + 2

    cave.set_rocks(
        [
            str(cave.cave_minx) + "," + str(floor_level) + " -> " +\
            str(cave.cave_maxx) + "," + str(floor_level)
        ]
    )
    cave.sand_coords = []
    cave.print_cave()

    cave.simulate_sand_floor()
    cave.print_cave()

    return 0 


if __name__ == "__main__":
    main()