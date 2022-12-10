import pathlib


def main():
    file_path = pathlib.Path(__file__)
    with open(file_path.parent.parent / "input" / file_path.stem) as file:
        instructions = [line.strip() for line in file]

    part1(instructions)
    part2(instructions)


def part1(instructions: list[str]):
    signals = []

    def capture_signal():
        if cycle == 20 or (cycle > 20 and (cycle - 20) % 40 == 0):
            signals.append(x * cycle)

    x = cycle = 1
    for instruction in instructions:
        match instruction.split():
            case ("noop", *_):
                cycle += 1
                capture_signal()
            case ("addx", val):
                cycle += 1
                capture_signal()
                cycle += 1
                x += int(val)
                capture_signal()

    print(sum(signals))


def part2(instructions: list[str]):
    screen_width = 40
    screen = [["." for _ in range(screen_width)] for _ in range(6)]

    def draw_pixel():
        row, column = divmod(cycle, screen_width)
        if column in (x - 1, x, x + 1):
            try:
                screen[row][column] = "#"
            except IndexError:
                pass

    cycle = 0
    x = 1
    for instruction in instructions:
        draw_pixel()
        match instruction.split():
            case ("noop", *_):
                cycle += 1
            case ("addx", val):
                cycle += 1
                draw_pixel()
                cycle += 1
                x += int(val)

    draw_pixel()

    # draw screen
    for row in screen:
        for i, pixel in enumerate(row):
            print(pixel, end="")
            if i == 39:
                print("\n", end="")


if __name__ == "__main__":
    main()
