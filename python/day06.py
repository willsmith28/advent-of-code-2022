import collections
import itertools
import pathlib
from collections.abc import Iterable
from typing import TypeVar

T = TypeVar("T")


def main():
    file_path = pathlib.Path(__file__)
    with open(file_path.parent.parent / "input" / file_path.stem) as file:
        data_stream = file.readline()

    find_start_of_message_marker(data_stream, 4)
    find_start_of_message_marker(data_stream, 14)


def find_start_of_message_marker(data_stream: str, window_size: int):
    for window in sliding_window(enumerate(data_stream), window_size):
        if len({char for _, char in window}) == window_size:
            print(window[-1][0] + 1)
            return


def sliding_window(iterable: Iterable[T], n: int) -> Iterable[tuple[T, ...]]:
    it = iter(iterable)
    window = collections.deque(itertools.islice(it, n), n)
    if len(window) == n:
        yield tuple(window)
    for item in it:
        window.append(item)
        yield tuple(window)


if __name__ == "__main__":
    main()
