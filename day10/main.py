import os
import time

DATA_PATH = "E:\\gitcode\\adventofcode_2022\\day10\\data.txt"


def get_sum_sig_strengths(data):
    sig_strength_idxs = list(range(19, 220, 40))

    register_history = []

    reg_X = 1

    next_reg_val = 1

    for i in data:
        register_history.append(next_reg_val)
        i_args = i.split(" ")

        if i_args[0] == "noop":
            next_reg_val = reg_X
            continue
        elif i_args[0] == "addx":
            register_history.append(next_reg_val)
            reg_X += int(i_args[1])
            next_reg_val = reg_X

    reg_sig_strength_vals = [register_history[i] * (i + 1) for i in sig_strength_idxs]
    return sum(reg_sig_strength_vals)


def get_sprite_pos_string(sprite_idx):
    sprite_string = [" "] * 40

    for i in range(sprite_idx - 1, sprite_idx + 2, 1):
        if i >= 0 and i <=39:
            sprite_string[i] = u"\u2588"
    
    return sprite_string


def draw_crt_screen(data):
    crt_screen = []

    register_history = []

    reg_X = 1
    next_reg_val = 1
    sprite_string = get_sprite_pos_string(reg_X)

    curr_crt_row = []

    cyc_num = 1

    for i in data:
        sprite_string = get_sprite_pos_string(reg_X)
        register_history.append(next_reg_val)
        i_args = i.split(" ")

        crt_draw_idx = (cyc_num - 1) % 40
        curr_crt_row.append(sprite_string[crt_draw_idx])

        print("Sprite position", "".join(sprite_string))
        print()
        print("Start cycle", str(cyc_num) + ": begin exec", i_args)
        print("During cycle", str(cyc_num) + ": CRT draw in pos", (cyc_num-1) % 40)
        print("Current CRT row:", "".join(curr_crt_row))
        print()
        cyc_num += 1
        if len(curr_crt_row) >= 40:
            crt_screen.append(curr_crt_row)
            curr_crt_row = []


        if i_args[0] == "noop":
            next_reg_val = reg_X
            continue
        elif i_args[0] == "addx":
            register_history.append(next_reg_val)
            crt_draw_idx = (cyc_num - 1) % 40
            curr_crt_row.append(sprite_string[crt_draw_idx])
            reg_X += int(i_args[1])
            next_reg_val = reg_X

            print("During cycle", str(cyc_num) + ": CRT draw in pos", (cyc_num-1) % 40)
            print("Current CRT row:", "".join(curr_crt_row))
            print("End of cycle", str(cyc_num) + ": finish executing", i_args, "(Regiser X is now", str(reg_X) + ")")
            cyc_num += 1

            if len(curr_crt_row) >= 40:
                crt_screen.append(curr_crt_row)
                curr_crt_row = []
        
    
    print(curr_crt_row, len(curr_crt_row))
    for row in crt_screen:
        print("".join(row))


def main():
    with open(DATA_PATH) as file:
        data = [line.rstrip("\n") for line in file]
    
    sum_sig_strengths = get_sum_sig_strengths(data)
    print("SUM SIG STRENGTHS:", sum_sig_strengths)
    draw_crt_screen(data)

    return 0 


if __name__ == "__main__":
    main()