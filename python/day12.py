import collections
import pathlib
from typing import TypeAlias

Position: TypeAlias = tuple[int, int]
AdjacencyList: TypeAlias = dict[Position, list[Position]]


def main():
    file_path = pathlib.Path(__file__)
    with open(file_path.parent.parent / "input" / file_path.stem) as file:
        grid = [line.strip() for line in file]

    adj_list, start, end = build_adj_list(grid)

    print(shortest_path(adj_list, start, end))
    possible_starting_pos = (
        (row, col)
        for row, line in enumerate(grid)
        for col, char in enumerate(line)
        if char in ("a", "S")
    )
    print(min(shortest_path(adj_list, start, end) for start in possible_starting_pos))


def build_adj_list(grid: list[list[str]]) -> tuple[AdjacencyList, Position, Position]:
    adj_list: AdjacencyList = collections.defaultdict(list)
    ROWS, COLS = len(grid), len(grid[0])
    for row, line in enumerate(grid):
        for col, char in enumerate(line):
            point = (row, col)
            if char == "S":
                start: Position = point
                char = "a"
            elif char == "E":
                end: Position = point
                char = "z"

            neighbors = (
                (row + 1, col),
                (row - 1, col),
                (row, col + 1),
                (row, col - 1),
            )
            current_position_val = ord(char)
            for nrow, ncol in neighbors:
                if nrow < 0 or nrow >= ROWS or ncol < 0 or ncol >= COLS:
                    continue

                nchar = grid[nrow][ncol]
                if nchar == "S":
                    nchar = "a"
                elif nchar == "E":
                    nchar = "z"

                if ord(nchar) - current_position_val <= 1:
                    adj_list[point].append((nrow, ncol))

    return adj_list, start, end


def shortest_path(adj_list: AdjacencyList, start: Position, end: Position) -> int:
    shortest_path_seen: dict[Position, int] = {start: 0}
    queue = collections.deque(((start, 0),))
    while queue:
        current_pos, steps = queue.popleft()
        next_steps = steps + 1
        for neighbor in adj_list[current_pos]:
            if (
                neighbor not in shortest_path_seen
                or next_steps < shortest_path_seen[neighbor]
            ):
                shortest_path_seen[neighbor] = next_steps
                if neighbor != end:
                    queue.append((neighbor, next_steps))

    try:
        return shortest_path_seen[end]
    except KeyError:
        return float("inf")


if __name__ == "__main__":
    main()
