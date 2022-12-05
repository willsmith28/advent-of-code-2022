import copy
import pathlib
import re
from typing import TypeAlias

Instruction: TypeAlias = tuple[int, str, str]
Stacks: TypeAlias = dict[str, list[str]]


def main():
    file_path = pathlib.Path(__file__)
    with open(file_path.parent.parent / "input" / file_path.stem) as file:
        initial_stacks: list[str] = []
        for line in file:
            if line == "\n":
                break
            initial_stacks.append(line)

        stacks = {
            stack: [line[i] for line in initial_stacks[-2::-1] if not line[i].isspace()]
            for i, stack in filter(
                lambda item: item[1].isdecimal(), enumerate(initial_stacks[-1])
            )
        }
        instructions: list[Instruction] = []
        for line in file:
            match = re.match(r"move (\d+) from (\d) to (\d)", line)
            amount, source, dest = match.groups()
            instructions.append((int(amount), source, dest))

    part1(copy.deepcopy(stacks), instructions)
    part2(stacks, instructions)


def part1(stacks: Stacks, instructions: list[Instruction]):
    for amount, source, dest in instructions:
        for _ in range(int(amount)):
            stacks[dest].append(stacks[source].pop())

    print("".join(stack[-1] for stack in stacks.values()))


def part2(stacks: Stacks, instructions: list[Instruction]):
    for amount, source, dest in instructions:
        crane = [stacks[source].pop() for _ in range(amount)]

        while crane:
            stacks[dest].append(crane.pop())

    print("".join(stack[-1] for stack in stacks.values()))


if __name__ == "__main__":
    main()
