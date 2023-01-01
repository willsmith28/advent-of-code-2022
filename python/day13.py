import itertools
import pathlib
from ast import literal_eval
from collections.abc import Iterable
from typing import TypeVar, Union

T = TypeVar("T")


class Packet(list):
    def __init__(self, iterable) -> None:
        super().__init__(
            item if isinstance(item, int) else Packet(item) for item in iterable
        )

    def __eq__(self, other: Union["Packet", int]) -> bool:
        if isinstance(self, Packet) and isinstance(other, Packet):
            for lhs, rhs in itertools.zip_longest(self, other, fillvalue=None):
                if lhs is not None and rhs is not None:
                    if isinstance(lhs, int) and isinstance(rhs, int):
                        if lhs == rhs:
                            continue
                        return False

                    elif isinstance(lhs, int) and isinstance(rhs, Packet):
                        lhs = Packet([lhs])
                        if lhs == rhs:
                            continue
                        return False

                    elif isinstance(lhs, Packet) and isinstance(rhs, int):
                        rhs = Packet([rhs])
                        if lhs == rhs:
                            continue
                        return False

                    elif isinstance(lhs, Packet) and isinstance(rhs, Packet):
                        if lhs == rhs:
                            continue
                        return False

                elif lhs is None or rhs is None:
                    return False
            return True

        elif isinstance(self, Packet) and isinstance(other, int):
            other = Packet([other])
            return self == other

        elif isinstance(self, int) and isinstance(other, Packet):
            other = Packet([self])
            return self == other

        raise TypeError(f"== is unsupported between {type(self)} and {type(other)}")

    def __lt__(self, other: Union["Packet", int]) -> bool:
        if isinstance(self, Packet) and isinstance(other, Packet):
            for lhs, rhs in itertools.zip_longest(self, other, fillvalue=None):
                if lhs is not None and rhs is not None:
                    if isinstance(lhs, int) and isinstance(rhs, int):
                        if lhs == rhs:
                            continue
                        return lhs < rhs

                    elif isinstance(lhs, int) and isinstance(rhs, Packet):
                        lhs = Packet([lhs])
                        if lhs == rhs:
                            continue
                        return lhs < rhs

                    elif isinstance(lhs, Packet) and isinstance(rhs, int):
                        rhs = Packet([rhs])
                        if lhs == rhs:
                            continue
                        return lhs < rhs

                    elif isinstance(lhs, Packet) and isinstance(rhs, Packet):
                        if lhs == rhs:
                            continue
                        return lhs < rhs

                elif lhs is None and rhs is not None:
                    return True

                elif lhs is not None and rhs is None:
                    return False
            return True

        elif isinstance(self, Packet) and isinstance(other, int):
            other = Packet([other])
            return self < other

        elif isinstance(self, int) and isinstance(other, Packet):
            other = Packet([self])
            return self < other

        raise TypeError(f"< is unsupported between {type(self)} and {type(other)}")


def main():
    file_path = pathlib.Path(__file__)
    with open(file_path.parent.parent / "input" / file_path.stem) as file:
        packets: list[Packet] = [
            Packet(literal_eval(line)) for line in file if line != "\n"
        ]

    part1(packets)
    part2(packets)


def part1(packets: list[Packet]):
    result = 0
    index = 1
    for p1, p2 in grouper(packets, 2):
        if p1 < p2:
            result += index
        index += 1

    print(result)


def part2(packets: list[Packet]):
    divider_packets = [Packet([[2]]), Packet([[6]])]
    packets = [*packets, *divider_packets]
    packets.sort()
    result = 1
    index = 1
    for packet in packets:
        for divider_packet in divider_packets:
            if packet == divider_packet:
                result *= index
                break
        index += 1

    print(result)


def grouper(iterable: Iterable[T], n: int) -> Iterable[tuple[T, ...]]:
    args = [iter(iterable)] * n
    return zip(*args, strict=True)


if __name__ == "__main__":
    main()
