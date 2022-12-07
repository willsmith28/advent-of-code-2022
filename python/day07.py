import functools
import operator
import pathlib
from collections.abc import Iterator
from typing import TextIO


class File:
    def __init__(self, name: str, size: int) -> None:
        self.name = name
        self.size = size


class Directory:
    def __init__(self, name) -> None:
        self.name = name
        self.files: dict[str, File] = {}
        self.directories: dict[str, Directory] = {}

    @functools.cached_property
    def size(self) -> int:
        file_sizes = sum(file.size for file in self.files.values())
        return file_sizes + sum(
            directory.size for directory in self.directories.values()
        )


class FileSystem:
    def __init__(self) -> None:
        self.root = Directory("")

    def add(self, path: str, item: File):
        root, *path = path.split("/")
        assert root == ""
        current = self.root
        for name in path:
            if name == "":
                continue
            elif name in current.directories:
                current = current.directories[name]
            else:
                current.directories[name] = Directory(name)
                current = current.directories[name]

        current.files[item.name] = item

    def iter_directories(self, current: Directory | None = None) -> Iterator[Directory]:
        if current is None:
            current = self.root

        yield current

        for sub_dir in current.directories.values():
            yield from self.iter_directories(sub_dir)


def main():
    file_path = pathlib.Path(__file__)
    with open(file_path.parent.parent / "input" / file_path.stem) as file:
        fs = build_file_system(file)

    part1(fs)
    part2(fs)


def part1(fs: FileSystem):
    print(sum(dir.size for dir in fs.iter_directories() if dir.size <= 100000))


def part2(fs: FileSystem):
    total_space = 70000000
    target_unused_space = 30000000
    directories = sorted(fs.iter_directories(), key=operator.attrgetter("size"))
    root = directories[-1]
    current_unused_space = total_space - root.size
    for dir in directories:
        if current_unused_space + dir.size >= target_unused_space:
            print(dir.size)
            return


def build_file_system(command_logs: TextIO):
    fs = FileSystem()
    command = next(command_logs).strip()
    assert command == "$ cd /"
    current_dir: list[str] = []
    current_dir_str = "/"
    for command in command_logs:
        command = command.strip()
        if command.startswith("$ cd "):
            # changing dirs
            dest_dir = command.split()[-1]
            if dest_dir == "..":
                current_dir.pop()
            else:
                current_dir.append(dest_dir)
        elif command == "$ ls":
            # consume results
            current_dir_str = f"/{'/'.join(current_dir)}"
        elif not command.startswith("$"):
            if command.startswith("dir"):
                continue
            else:
                size, file_name = command.split()
                fs.add(current_dir_str, File(file_name, int(size)))
    return fs


if __name__ == "__main__":
    main()
