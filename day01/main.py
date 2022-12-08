import os

DATA_PATH = "E:\\gitcode\\adventofcode_2022\\day01\\data.txt"

def main():
    with open(DATA_PATH) as file:
        lines = [line.rstrip() for line in file]
    data_splits = []
    curr_data = []
    for p in lines:
        if p == '':
            data_splits.append(curr_data)
            curr_data = []
        else:
            curr_data.append(float(p))
    print("Data splits:", data_splits)
    
    data_sum = list(map(sum, data_splits))
    print("Data sums:", data_sum)
    
    sort_data = sorted(data_sum, reverse=True)
    print("Sorted data:", sort_data)
    print("Top 3 Sum:", sum(sort_data[0:3]))
    return 0


if __name__ == "__main__":
    main()