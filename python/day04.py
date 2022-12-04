import pathlib
from typing import TypeAlias

Section: TypeAlias = tuple[int, int]
Assignment: TypeAlias = tuple[Section, Section]


def main():
    file_path = pathlib.Path(__file__)
    with open(file_path.parent.parent / "input" / file_path.stem) as file:
        assignments: list[Assignment] = []
        for line in file:
            section1, section2 = line.strip().split(",")
            assignments.append(
                (
                    tuple(map(int, section1.split("-"))),
                    tuple(map(int, section2.split("-"))),
                )
            )
    part1(assignments)
    part2(assignments)


def part1(assignments: list[Assignment]):
    print(
        sum(
            1
            for ((a, b), (c, d)) in assignments
            if a <= c <= d <= b or c <= a <= b <= d
        )
    )


def part2(assignments: list[Assignment]):
    print(
        len(assignments) - sum(1 for ((a, b), (c, d)) in assignments if b < c or d < a)
    )


if __name__ == "__main__":
    main()
