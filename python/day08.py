import pathlib


def main():
    file_path = pathlib.Path(__file__)
    with open(file_path.parent.parent / "input" / file_path.stem) as file:
        forest = [list(map(int, line.strip())) for line in file]

    visible_trees = part1(forest)
    part2(forest, visible_trees)


def part1(forest: list[list[int]]):
    ROWS, COLS = len(forest), len(forest[0])
    visible_trees = set()
    # add exterior
    # top row
    visible_trees.update((0, i) for i in range(COLS))
    # bottom row
    visible_trees.update((COLS - 1, i) for i in range(COLS))
    # left column
    visible_trees.update((i, 0) for i in range(ROWS))
    # right column
    visible_trees.update((i, ROWS - 1) for i in range(ROWS))
    # from (1,1) to (len(forst) - 2, len(forst[0]) - 2)
    for row in range(1, ROWS - 1):
        for col in range(1, COLS - 1):
            if (
                all(forest[row][col] > forest[row][i] for i in range(col - 1, -1, -1))
                or all(forest[row][col] > forest[row][i] for i in range(col + 1, COLS))
                or all(
                    forest[row][col] > forest[i][col] for i in range(row - 1, -1, -1)
                )
                or all(forest[row][col] > forest[i][col] for i in range(row + 1, ROWS))
            ):
                visible_trees.add((row, col))

    print(len(visible_trees))
    return visible_trees


def part2(forest: list[list[int]], visible_trees: set[tuple[int, int]]):
    ROWS, COLS = len(forest), len(forest[0])
    result = 0
    for (row, col) in visible_trees:
        if row == 0 or row == ROWS - 1 or col == 0 or col == COLS - 1:
            continue
        # look up
        up_count = 0
        for i in range(row - 1, -1, -1):
            up_count += 1
            if forest[row][col] <= forest[i][col]:
                break

        # look down
        down_count = 0
        for i in range(row + 1, ROWS):
            down_count += 1
            if forest[row][col] <= forest[i][col]:
                break

        # look left
        left_count = 0
        for i in range(col - 1, -1, -1):
            left_count += 1
            if forest[row][col] <= forest[row][i]:
                break

        # look right
        right_count = 0
        for i in range(col + 1, COLS):
            right_count += 1
            if forest[row][col] <= forest[row][i]:
                break

        result = max(result, up_count * down_count * left_count * right_count)

    print(result)


if __name__ == "__main__":
    main()
