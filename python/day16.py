import collections
import itertools
import pathlib
import re


def main():
    file_path = pathlib.Path(__file__)
    with open(file_path.parent.parent / "input" / file_path.stem) as file:
        adj_list = collections.defaultdict(list)
        flow_rates = {}
        for line in file:
            match = re.match(
                r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnel(?:s)? lead(?:s)? to"
                r" valve(?:s)? ([A-Z]{2}(?:, [A-Z]{2})*)",
                line,
            )
            assert match
            valve, flow_rate, neighbors = match.groups()
            flow_rates[valve] = int(flow_rate)
            for neighbor in neighbors.split(", "):
                adj_list[valve].append(neighbor)

    for neighbors in adj_list.values():
        neighbors.sort(key=lambda neighbor: flow_rates[neighbor], reverse=True)

    # part1(adj_list, flow_rates)
    part2(adj_list, flow_rates)


def part1(adj_list: dict[str, list[str]], flow_rates: dict[str, int]):
    open_valves: frozenset[str]
    result = 0
    queue = collections.deque((("AA", frozenset(), 0, 1),))
    all_open_valves = {position for position, rate in flow_rates.items() if rate > 0}
    states = set()
    while queue:
        position, open_valves, released_pressure, current_time = queue.popleft()
        if current_time > 30:
            result = max(result, released_pressure)
            continue

        for valve in open_valves:
            released_pressure += flow_rates[valve]

        # print(
        #     f"current time: {current_time}; current position {position}; open valves"
        #     f" {', '.join(open_valves)} released pressure {released_pressure}"
        # )
        next_time = current_time + 1
        if open_valves == all_open_valves:
            queue.append((position, open_valves, released_pressure, next_time))
            continue

        # open valve
        if flow_rates[position] > 0 and position not in open_valves:
            open_valves = frozenset((*open_valves, position))
            states.add((position, open_valves, released_pressure, next_time))
            queue.append((position, open_valves, released_pressure, next_time))
            continue

        # move
        for neighbor in adj_list[position]:
            next_move = (neighbor, open_valves, released_pressure, next_time)
            # remove equivalent paths
            if next_move in states:
                continue
            states.add(next_move)
            queue.append(next_move)

    print(result)


def part2(adj_list: dict[str, list[str]], flow_rates: dict[str, int]):
    open_valves: frozenset[str]
    result = 0
    queue = collections.deque(((("AA", "AA"), frozenset(), 0, 1),))
    all_open_valves = {position for position, rate in flow_rates.items() if rate > 0}
    states = {}
    while queue:
        (
            (my_pos, elephant_pos),
            open_valves,
            released_pressure,
            current_time,
        ) = queue.popleft()
        if current_time > 26:
            result = max(result, released_pressure)
            continue

        for valve in open_valves:
            released_pressure += flow_rates[valve]

        next_time = current_time + 1
        if open_valves == all_open_valves:
            queue.append(
                (
                    (my_pos, elephant_pos),
                    open_valves,
                    released_pressure,
                    next_time,
                )
            )
            continue

        my_action_used = False
        elephant_action_used = False

        if flow_rates[my_pos] > 0 and my_pos not in open_valves:
            open_valves = frozenset((*open_valves, my_pos))
            my_action_used = True

        if flow_rates[elephant_pos] > 0 and elephant_pos not in open_valves:
            open_valves = frozenset((*open_valves, elephant_pos))
            elephant_action_used = True

        if my_action_used and elephant_action_used:
            states[((my_pos, elephant_pos), open_valves, next_time)] = released_pressure
            queue.append(
                ((my_pos, elephant_pos), open_valves, released_pressure, next_time)
            )
        elif my_action_used and not elephant_action_used:
            for elephant_neighbor in adj_list[elephant_pos]:
                next_move = (
                    (my_pos, elephant_neighbor),
                    open_valves,
                    next_time,
                )
                if next_move in states and released_pressure <= states[next_move]:
                    continue
                states[next_move] = released_pressure
                queue.append(
                    (
                        (my_pos, elephant_neighbor),
                        open_valves,
                        released_pressure,
                        next_time,
                    )
                )
        elif not my_action_used and elephant_action_used:
            for my_neighbor in adj_list[my_pos]:
                next_move = (
                    (my_neighbor, elephant_pos),
                    open_valves,
                    next_time,
                )
                if next_move in states and released_pressure <= states[next_move]:
                    continue
                states[next_move] = released_pressure
                queue.append(
                    (
                        (my_neighbor, elephant_pos),
                        open_valves,
                        released_pressure,
                        next_time,
                    )
                )
        else:
            for my_neighbor, elephant_neighbor in itertools.product(
                adj_list[my_pos], adj_list[elephant_pos]
            ):
                next_move = (
                    (my_neighbor, elephant_neighbor),
                    open_valves,
                    next_time,
                )
                if next_move in states and released_pressure <= states[next_move]:
                    continue
                states[next_move] = released_pressure
                queue.append(
                    (
                        (my_neighbor, elephant_neighbor),
                        open_valves,
                        released_pressure,
                        next_time,
                    )
                )

    print(result)


if __name__ == "__main__":
    main()
