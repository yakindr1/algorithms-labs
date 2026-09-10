"""Прогон сортировок по размерам и профилям данных, выгрузка в CSV."""

import argparse
import csv
import sys
import time
from pathlib import Path

import generators
import sorts

SIZES_QUADRATIC = [100, 200, 500, 1000, 2000, 3000]
SIZES_FAST = [100, 1000, 10_000, 50_000]


def repeats(n):
    """Берём минимум по многим прогонам.

    Одиночный замер на нагруженной машине ошибается вдвое: сравнение
    времени с числом операций это ловит сразу.
    """
    if n <= 1000:
        return 15
    return 7 if n <= 2000 else 5


def run_one(name, profile, n, seed):
    fn = sorts.ALGORITHMS[name]
    data = generators.make(profile, n, seed=seed)
    expected = sorted(data)

    st = sorts.new_stats()
    check = list(data)
    fn(check, st)

    best = None
    for _ in range(repeats(n)):
        a = list(data)
        t0 = time.perf_counter()
        fn(a, sorts.new_stats())
        dt = time.perf_counter() - t0
        best = dt if best is None else min(best, dt)

    return {
        "algorithm": name,
        "profile": profile,
        "n": n,
        "comparisons": st[sorts.CMP],
        "assignments": st[sorts.ASG],
        "seconds": round(best, 6),
        "correct": int(check == expected),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results.csv")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--max-quadratic", type=int, default=SIZES_QUADRATIC[-1])
    ap.add_argument("--max-fast", type=int, default=SIZES_FAST[-1])
    args = ap.parse_args()

    rows = []
    for name in sorts.ALGORITHMS:
        limit = args.max_quadratic if name in sorts.QUADRATIC else args.max_fast
        sizes = SIZES_QUADRATIC if name in sorts.QUADRATIC else SIZES_FAST
        for n in [s for s in sizes if s <= limit]:
            for profile in generators.PROFILES:
                row = run_one(name, profile, n, args.seed)
                rows.append(row)
                print("%-13s %-14s n=%-6d cmp=%-12d asg=%-12d %.4f s"
                      % (name, profile, n, row["comparisons"],
                         row["assignments"], row["seconds"]), flush=True)

    out = Path(args.out)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print("записано строк:", len(rows), "->", out)


if __name__ == "__main__":
    sys.exit(main())
