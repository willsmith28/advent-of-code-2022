import pathlib


def main():
    file_path = pathlib.Path(__file__)
    with open(file_path.parent.parent / "input" / file_path.stem) as file:
        guide = [line.strip() for line in file]

    part1(guide)
    part2(guide)


def part1(guide: list[str]):
    """
    A, X = Rock     1 pt
    B, Y = Paper    2 pt
    C, Z = Scissors 3 pt
    win     6 pt
    lose    0 pt
    draw    3 pt
    """
    round_results = {  # throw + outcome
        "A X": 4,  # 1 + 3
        "A Y": 8,  # 2 + 6
        "A Z": 3,  # 3 + 0
        "B X": 1,  # 1 + 0
        "B Y": 5,  # 2 + 3
        "B Z": 9,  # 3 + 6
        "C X": 7,  # 1 + 6
        "C Y": 2,  # 2 + 0
        "C Z": 6,  # 3 + 3
    }
    print(sum(round_results[round] for round in guide))


def part2(guide: list[str]):
    """
    A = Rock        1 pt
    B = Paper       2 pt
    C = Scissors    3 pt
    X = Lose        0 pt
    Y = Draw        3 pt
    Z = Win         6 pt
    """
    round_results = {  # throw + outcome
        "A X": 3,  # 3 + 0
        "A Y": 4,  # 1 + 3
        "A Z": 8,  # 2 + 6
        "B X": 1,  # 1 + 0
        "B Y": 5,  # 2 + 3
        "B Z": 9,  # 3 + 6
        "C X": 2,  # 2 + 0
        "C Y": 6,  # 3 + 3
        "C Z": 7,  # 1 + 6
    }
    print(sum(round_results[round] for round in guide))


if __name__ == "__main__":
    main()
