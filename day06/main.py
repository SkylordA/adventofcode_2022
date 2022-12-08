import os

DATA_PATH = "E:\\gitcode\\adventofcode_2022\\day06\\data.txt"

def find_first_n_diff_chars(n, data_str):
    buffer = []

    curr_idx = 0

    for i in range(n):
        buffer.insert(0, data_str[curr_idx])
        curr_idx += 1
    
    found = False

    while not found:
        if len(set(buffer)) == n:
            print(buffer)
            found = True
        else:
            buffer.pop()
            buffer.insert(0, data_str[curr_idx])
            curr_idx += 1
        
        assert curr_idx < len(data_str), "RAN OUT OF DATA"

    return curr_idx



def main():
    with open(DATA_PATH) as file:
        data = [line.rstrip("\n") for line in file]
    
    print(find_first_n_diff_chars(4, data[0]))
    print(find_first_n_diff_chars(14, data[0]))

    return 0


if __name__ == "__main__":
    main()