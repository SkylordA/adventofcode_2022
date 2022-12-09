import os
import numpy as np
import curses
import time

DATA_PATH = "E:\\gitcode\\adventofcode_2022\\day09\\data.txt"

def print_map(map):
    h, w = map.shape

    for i in range(h-1, -1, -1):
        row_str = ""
        for j in range(w):
            row_str += str(map[i][j], "utf-8")
        print(row_str)


def print_map_curses(map, stdcsr):
    h, w = map.shape
    rows, cols = stdcsr.getmaxyx()
    start_k = h - rows
    map_str = ""
    for i in range(h-1, -1, -1):
        row_str = ""
        for j in range(w):
            row_str += str(map[i][j], "utf-8")
        k = (h - 1) - i
        try:
            if k > start_k:
                stdcsr.addstr(k - start_k, 0, row_str)
        except curses.error:
            pass
    stdcsr.refresh()
    time.sleep(0.01)


def generate_full_empty_map(data):
    curr_x = 0
    curr_y = 0

    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0

    for d in data:
        direction, amount = d.split()
        amount = int(amount)

        if direction == "U": curr_y += amount
        if direction == "D": curr_y -= amount
        if direction == "R": curr_x += amount
        if direction == "L": curr_x -= amount
        min_x = min(curr_x, min_x)
        max_x = max(curr_x, max_x)
        min_y = min(curr_y, min_y)
        max_y = max(curr_y, max_y)

    map = np.chararray((max_y - min_y + 1, max_x - min_x + 1))
    map[:] = "."

    start_pos = [-min_x, -min_y]
    map[-min_y][-min_x] = "s"
    return map, start_pos


def determine_next_tpos(hpos, tpos):
    xdiff = hpos[0] - tpos[0]
    ydiff = hpos[1] - tpos[1]
    xdir = int(xdiff / abs(xdiff)) if xdiff != 0 else 1
    ydir = int(ydiff / abs(ydiff)) if ydiff != 0 else 1

    assert abs(xdiff) <= 2, "TOO BIG OF A X DIFFERENCE"
    assert abs(ydiff) <= 2, "TOO BIG OF A Y DIFFERENCE"
    if abs(xdiff) > 1:
        if abs(ydiff) >= 1:
            tpos[0] += 1 * xdir
            tpos[1] += 1 * ydir
        else:
            tpos[0] += 1 * xdir
    elif abs(ydiff) > 1:
        if abs(xdiff) >= 1:
            tpos[1] += 1 * ydir
            tpos[0] += 1 * xdir
        else:
            tpos[1] += 1 * ydir
    return tpos


def run_map_data(map, start_pos, data, num_tails = 1):
    # stdscr = curses.initscr()
    # stdscr.clear()

    hpos = np.copy(start_pos)
    tails = []
    for _ in range(num_tails):
        tails.append(np.copy(start_pos))
    draw_map = np.copy(map)
    draw_map[start_pos[1]][start_pos[0]] = "s"

    for d in data:
        direction, amount = d.split()
        amount = int(amount)
        for i in range(amount):
            draw_map[hpos[1]][hpos[0]] = "."
            for i in range(num_tails - 1, -1, -1):
                draw_map[tails[i][1]][tails[i][0]] = "."
            draw_map[start_pos[1]][start_pos[0]] = "s"
            
            if direction == "U": hpos[1] += 1
            if direction == "D": hpos[1] -= 1
            if direction == "R": hpos[0] += 1
            if direction == "L": hpos[0] -= 1

            try:
                assert hpos[0] < map.shape[1]
                assert hpos[1] < map.shape[0]
            except AssertionError as e:
                import pdb; pdb.set_trace()

            curr_head = np.copy(hpos)
            for i in range(num_tails):
                curr_tail = tails[i]
                tails[i] = determine_next_tpos(curr_head, curr_tail)
                curr_head = np.copy(tails[i])
            map[tails[-1][1]][tails[-1][0]] = "#"
            
            draw_map[tails[-1][1]][tails[-1][0]] = "#"
            for i in range(num_tails - 1, -1, -1):
                draw_map[tails[i][1]][tails[i][0]] = str(i + 1)
            draw_map[hpos[1]][hpos[0]] = "H"

            # print_map_curses(draw_map, stdscr)

    # curses.endwin()
    return map


def main():
    with open(DATA_PATH) as file:
        data = [line.rstrip("\n") for line in file]

    map, start_pos = generate_full_empty_map(data)
    map = run_map_data(map, start_pos, data, 9)
    print_map(map)

    num_tail_pos = np.sum(np.char.find(map, '#'.encode("utf-8")) != -1)
    print("Num tail pos:", num_tail_pos)
    
    return 0 


if __name__ == "__main__":
    main()