import pathlib
from typing import TypeAlias

Point: TypeAlias = tuple[int, int]
SAND_SOURCE: Point = (500, 0)


def main():
    file_path = pathlib.Path(__file__)
    with open(file_path.parent.parent / "input" / file_path.stem) as file:
        rocks: set[Point] = set()
        for line in file:
            points = [tuple(map(int, point.split(","))) for point in line.split(" -> ")]
            for i in range(1, len(points)):
                sx, sy = points[i - 1]
                ex, ey = points[i]
                if sx == ex:
                    rocks.update((sx, j) for j in range(min(sy, ey), max(sy, ey) + 1))
                elif sy == ey:
                    rocks.update((j, sy) for j in range(min(sx, ex), max(sx, ex) + 1))
                else:
                    raise ValueError("bad input")

    lowest_rock = max(y for _, y in rocks)
    sand = part1(rocks, lowest_rock)
    part2(rocks, sand, lowest_rock)


def part1(rocks: set[Point], lowest_rock: int) -> set[Point]:
    sand: set[Point] = set()
    while True:
        sand_unit: Point = SAND_SOURCE
        while sand_unit[1] < lowest_rock:
            # potential position
            next_pos: Point = (sand_unit[0], sand_unit[1] + 1)
            # sand can move down
            if next_pos not in rocks and next_pos not in sand:
                sand_unit = next_pos
                continue

            # try left
            left_pos = (next_pos[0] - 1, next_pos[1])
            if left_pos not in rocks and left_pos not in sand:
                sand_unit = left_pos
                continue

            # try right
            right_pos = (next_pos[0] + 1, next_pos[1])
            if right_pos not in rocks and right_pos not in sand:
                sand_unit = right_pos
                continue

            # final resting position
            sand.add(sand_unit)
            break
        else:
            # falls into the abyss
            break

    print(len(sand))
    return sand


def part2(rocks: set[Point], sand: set[Point], lowest_rock: int):
    floor = lowest_rock + 2
    while True:
        sand_unit = SAND_SOURCE
        while SAND_SOURCE not in sand:
            # potential position
            next_pos: Point = (sand_unit[0], sand_unit[1] + 1)
            # reached floor
            if next_pos[1] == floor:
                sand.add(sand_unit)
                break

            # sand can move down
            if next_pos not in rocks and next_pos not in sand:
                sand_unit = next_pos
                continue

            # try left
            left_pos = (next_pos[0] - 1, next_pos[1])
            if left_pos not in rocks and left_pos not in sand:
                sand_unit = left_pos
                continue

            # try right
            right_pos = (next_pos[0] + 1, next_pos[1])
            if right_pos not in rocks and right_pos not in sand:
                sand_unit = right_pos
                continue

            # final resting position
            sand.add(sand_unit)
            break
        else:
            assert SAND_SOURCE in sand
            break

    print(len(sand))


if __name__ == "__main__":
    main()
