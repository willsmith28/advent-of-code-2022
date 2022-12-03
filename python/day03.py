import pathlib
from collections.abc import Iterable
from typing import TypeVar

T = TypeVar("T")


def main():
    file_path = pathlib.Path(__file__)
    with open(file_path.parent.parent / "input" / file_path.stem) as file:
        rucksacks = [line.strip() for line in file]

    part1(rucksacks)
    part2(rucksacks)


def part1(rucksacks: list[str]):
    total = 0
    for rucksack in rucksacks:
        mid = len(rucksack) // 2
        compartment1, compartment2 = rucksack[:mid], rucksack[mid:]
        (item,) = set(compartment1).intersection(compartment2)
        total += item_to_priority(item)

    print(total)


def part2(rucksacks: list[str]):
    total = 0
    for rucksack1, rucksack2, rucksack3 in grouper(rucksacks, 3):
        (badge,) = set(rucksack1).intersection(rucksack2, rucksack3)
        total += item_to_priority(badge)

    print(total)


def item_to_priority(item: str) -> int:
    assert len(item) == 1
    char_val = ord(item)
    if 97 <= char_val <= 122:
        # lowercase
        return char_val - 96
    elif 65 <= char_val <= 90:
        # uppercase
        return char_val - 38

    raise ValueError("item must be a-zA-Z")


def grouper(iterable: Iterable[T], n: int) -> Iterable[tuple[T, ...]]:
    args = [iter(iterable)] * n
    return zip(*args, strict=True)


if __name__ == "__main__":
    main()
