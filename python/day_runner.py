import importlib.util
import pathlib
import sys
import time


def main():
    day_runner_path = pathlib.Path(__file__)
    module_paths = (
        path
        for path in day_runner_path.parent.iterdir()
        if path.is_file() and path.stem != day_runner_path.stem
    )
    total_time = 0
    for day in sorted(module_paths, key=lambda item: item.stem):
        # import day module from path
        spec = importlib.util.spec_from_file_location(day.stem, day)
        module = importlib.util.module_from_spec(spec)
        sys.modules[day.stem] = module
        spec.loader.exec_module(module)

        # execute solution
        print(day.stem)
        t0 = time.perf_counter()
        module.main()
        t1 = time.perf_counter()
        delta = t1 - t0
        print("time taken", delta, "\n")
        total_time += delta

    print("total time", total_time)


if __name__ == "__main__":
    main()
