import os
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

DATA_PATH = "E:\\gitcode\\adventofcode_2022\\day07\\data.txt"


class FilesystemObject(ABC):
    def __init__(self, name: str, size: int, parent: Optional["FilesystemObject"]):
        self.name = name
        self.size = size
        self.parent = parent
    
    @abstractmethod
    def print(level: int):
        pass


class Directory(FilesystemObject):
    def __init__(self, name: str, size: int, parent: Optional[FilesystemObject]):
        super().__init__(name, size, parent)
        self.contents = []
    
    def add_content(self, content: FilesystemObject):
        self.contents.append(content)
    
    def get_subdir(self, name: str):
        for c in self.contents:
            if isinstance(c, Directory):
                if c.name == name:
                    return c
        assert False, "COULDN'T FIND SUBDIR " + name

    def get_all_dir_sizes(self) -> List[int]:
        dir_sizes = sum(
            [c.get_all_dir_sizes() for c in self.contents if isinstance(c, Directory)], []
        )
        dir_sizes.insert(0, self.size)
        return dir_sizes

    def get_smallest_dir_that_matches(self, required_space) -> Tuple[bool, List["Directory"]]:
        contains_possible_match = self.size >= required_space
        
        if not contains_possible_match:
            return False, []

        subdirs_contain_possible_match = False
        subdirs = []
        
        for c in self.contents:
            if isinstance(c, Directory):
                scpm, sd = c.get_smallest_dir_that_matches(required_space)
                subdirs_contain_possible_match = subdirs_contain_possible_match or scpm
                if scpm:
                    subdirs = sum([subdirs, sd], [])
        
        if subdirs_contain_possible_match:
            dirs = subdirs
        else:
            dirs = [self]

        return contains_possible_match, dirs
    def populate_dir_sizes(self) -> int:
        self.size = sum([c.populate_dir_sizes() for c in self.contents])
        return self.size

    def print(self, level: int):
        print("".join(["  "] * level), "-", self.name, "(dir, size=" + str(self.size) + ")")
        for c in self.contents:
            c.print(level + 1)


class File(FilesystemObject):
    def __init__(self, name: str, size: int, parent: Optional[FilesystemObject]):
        super().__init__(name, size, parent)

    def populate_dir_sizes(self) -> int:
        return self.size

    def print(self, level: int):
        print("".join(["  "] * level), "-", self.name, "(file, size=" + str(self.size) + ")")


def generate_file_system(data: List[str]) -> FilesystemObject:
    root_dir = Directory("/", -1, None)
    
    current_dir = root_dir

    for line in data:
        line_contents = line.split()
        if line_contents[0] == "$":
            if line_contents[1] == "cd":
                if line_contents[2] == "/":
                    current_dir = root_dir
                elif line_contents[2] == "..":
                    current_dir = current_dir.parent
                else:
                    current_dir = current_dir.get_subdir(line_contents[2])
            elif line_contents[1] == "ls":
                continue
        elif line_contents[0] == "dir":
            current_dir.add_content(
                Directory(line_contents[1], -1, current_dir)
            )
        else:
            current_dir.add_content(
                File(line_contents[1], int(line_contents[0]), current_dir)
            )

    return root_dir


def find_smallest_dir(root_dir: Directory, required_space) -> Directory:
    _, dirs = root_dir.get_smallest_dir_that_matches(required_space)
    smallest_dir = None

    for d in dirs:
        size = d.size
        if smallest_dir is None:
            smallest_dir = d
        else:
            if smallest_dir.size > size:
                smallest_dir = d
    return smallest_dir


def main():
    with open(DATA_PATH) as file:
        data = [line.rstrip("\n") for line in file]
    root_dir = generate_file_system(data)   
    root_dir.populate_dir_sizes()
    root_dir.print(0)
    dir_sizes = root_dir.get_all_dir_sizes()

    filtered_dir_sizes = [ds for ds in dir_sizes if ds <= 100000]
    
    print("SUM DIRS < 100000:", sum(filtered_dir_sizes))    

    total_space = 70000000
    max_required_space = 30000000
    used_space = root_dir.size

    required_space = max_required_space - (total_space - used_space)
    print("REQUIRED SPACE:", required_space)
    dir = find_smallest_dir(root_dir, required_space)

    print("Smallest dir to delete size:", dir.size)

    return 0


if __name__ == "__main__":
    main()