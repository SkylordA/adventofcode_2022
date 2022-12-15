import os
import numpy as np
from tqdm import tqdm

DATA_PATH = "E:\\gitcode\\adventofcode_2022\\day15\\data.txt"


class SensorBeaconPair:
    def __init__(self, sensor_coords, beacon_coords):
        self.sensor_coords = sensor_coords
        self.beacon_coords = beacon_coords
        self.manhattan_distance = self._calculate_manhattan_distance()
        self.pos_lines, self.neg_lines = self._calculate_edge_lines()
    
    def _calculate_manhattan_distance(self):
        sx, sy = self.sensor_coords
        bx, by = self.beacon_coords
        return abs(bx - sx) + abs(by - sy)
    
    def _calculate_edge_lines(self):
        pos_lines = []
        neg_lines = []
        sx, sy = self.sensor_coords
        pxmax = (sx + self.manhattan_distance, sy)
        pxmin = (sx - self.manhattan_distance, sy)
        pymax = (sx, sy + self.manhattan_distance)
        pymin = (sx, sy - self.manhattan_distance)
        
        mpos = 1
        mneg = -1
        pos_lines.append((mpos, pxmin[1] - mpos * pxmin[0]))
        pos_lines.append((mpos, pxmax[1] - mpos * pxmax[0]))
        neg_lines.append((mneg, pxmin[1] - mneg * pxmin[0]))
        neg_lines.append((mneg, pxmax[1] - mneg * pxmax[0]))
        return pos_lines, neg_lines



class Cave:
    def __init__(self):
        self.sb_pairs = []
        self.range_coords = []
        self.cave_minx = float("inf")
        self.cave_maxx = -float("inf")
        self.cave_miny = float("inf")
        self.cave_maxy = -float("inf")
    
    def _string_to_signed_int(self, intstr):
        if intstr[0] == "-":
            return int(intstr[1:]) * -1
        else:
            return int(intstr)
        
    def create_sb_pairs(self, data):
        for l in data:
            components = l.split(" ")

            sx = self._string_to_signed_int(components[2][2:][:-1])
            sy = self._string_to_signed_int(components[3][2:][:-1])
            bx = self._string_to_signed_int(components[8][2:][:-1])
            by = self._string_to_signed_int(components[9][2:])
            
            self.cave_minx = min([self.cave_minx, sx, bx])
            self.cave_maxx = max([self.cave_maxx, sx, bx])
            self.cave_miny = min([self.cave_miny, sy, by])
            self.cave_maxy = max([self.cave_maxy, sy, by])

            sbpair = SensorBeaconPair((sx, sy), (bx, by))
            self.sb_pairs.append(sbpair)
    
    def get_manhattan_coords(self, center_coords, manhattan_distance):
        coords = [center_coords]
        
        cx, cy = center_coords
        for dist in tqdm(range(1, manhattan_distance + 1)):
            for i in range(0, dist+1):
                mx1 = cx + i
                my1 = cy + (dist-i)
                
                mx2 = cx - i
                my2 = cy + (dist-i)
                
                mx3 = cx + i
                my3 = cy - (dist-i)
                
                mx4 = cx - i
                my4 = cy - (dist-i)

                range_coords = [(mx1, my1), (mx2, my2), (mx3, my3), (mx4, my4)]

                for x, y in range_coords:
                    self.cave_minx = min(self.cave_minx, x)
                    self.cave_maxx = max(self.cave_maxx, x)
                    self.cave_miny = min(self.cave_miny, y)
                    self.cave_maxy = max(self.cave_maxy, y)

                coords.extend(range_coords)

        coords = list(set(coords))
        return coords


    def populate_range_coords(self):
        for sbpair in tqdm(self.sb_pairs):
            coords = self.get_manhattan_coords(sbpair.sensor_coords, sbpair.manhattan_distance)
            self.range_coords.extend(coords)
        self.range_coords = list(set(self.range_coords))
        pass
    
    def count_at_y(self, y):
        count = 0
        # Range values based on looking at max manhattan distance and min/max sensor locations
        for x in tqdm(range(-2000000, 6000000)):
            valid = False
            for sbpair in self.sb_pairs:
                sx, sy = sbpair.sensor_coords
                bx, by = sbpair.beacon_coords
                if sbpair.manhattan_distance >=\
                    (abs(x - sx) + abs(y - sy)) and\
                        (bx != x or by != y):
                    valid = valid or True
            
            if valid:
                count += 1

        return count

    def get_freq_in_range(self, minimum, maximum):
        pos_lines = []
        neg_lines = []

        for sbp in self.sb_pairs:
            pos_lines.extend(sbp.pos_lines)
            neg_lines.extend(sbp.neg_lines)
        
        bpos_line = None
        for i, a in enumerate(pos_lines):
            for j, b, in enumerate(pos_lines):
                if i > j or a[1] == b[1]:
                    continue
                if abs(a[1] - b[1]) == 2:
                    bpos_line = (1, (a[1] + b[1])/2)
        
        bneg_line = None
        for i, a in enumerate(neg_lines):
            for j, b, in enumerate(neg_lines):
                if i > j or a[1] == b[1]:
                    continue
                if abs(a[1] - b[1]) == 2:
                    bneg_line = (-1, (a[1] + b[1])/2)

        xpos = (bneg_line[1] - bpos_line[1]) / (bpos_line[0] - bneg_line[0])
        ypos = (bpos_line[0] * xpos) + bpos_line[1]
        return ((4000000 * xpos) + ypos)

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

        # Set Range coords
        for x, y in self.range_coords:
            j = y - self.cave_miny + 3
            i = x - self.cave_minx + 3
            charar[j][i] = "#"

        # Set Sensors and Beacons
        for sbpair in self.sb_pairs:
            sx, sy = sbpair.sensor_coords
            bx, by = sbpair.beacon_coords
            j = sy - self.cave_miny + 3
            i = sx - self.cave_minx + 3
            charar[j][i] = "S"
            j = by - self.cave_miny + 3
            i = bx - self.cave_minx + 3
            charar[j][i] = "B"
        
        # Print Cave
        for s in charar:
            string = ""
            for c in s:
                string += c
            print(string)

def main():
    with open(DATA_PATH) as file:
        data = [line.rstrip("\n") for line in file]

    cave = Cave()
    print("Create pairs...")
    cave.create_sb_pairs(data)

    # Slow
    # print("Populate range coords...")
    # cave.populate_range_coords()
    # print("Print...")
    # cave.print_cave()

    level = 2000000
    print("Count at y...")
    count = cave.count_at_y(level)
    print("Num position beacon not at level", str(level) + ":", count)
    
    minimum = 0
    maximum = 4000000
    freq = cave.get_freq_in_range(minimum, maximum)
    print("Frequency:", freq)


    return 0 


if __name__ == "__main__":
    main()