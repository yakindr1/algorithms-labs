"""Прогон решений на примерах из условий.

Запуск из папки contest. Файлы .cpp предварительно собрать:
    g++ -O2 -std=c++17 -o A_111156_selection_sort.exe A_111156_selection_sort.cpp
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

TESTS = [
    ("A_111156_selection_sort", "1 4 2 3 4", "4 4 3 2 1"),
    ("B_111157_insertion_sort", "1 4 2 3 4", "1 2 3 4 4"),
    ("C_111158_bubble_sort", "1 4 2 3 4", "4 4 3 2 1"),
    ("D_1411_bubble_swaps", "5\n1 2 3 4 5\n", "0"),
    ("D_1411_bubble_swaps", "5\n5 4 3 2 1\n", "10"),
    ("G_111166_counting_sort", "7 3 4 2 5", "2 3 4 5 7"),
    ("E_766_merge_sort", "2\n3 1\n", "1 3"),
    ("F_733_quick_sort", "2\n3 1\n", "1 3"),
    ("H_325_sort_points", "2\n1 2\n2 3\n", "1 2 2 3"),
    ("I_1406_anagrams", "sharm\nmarsh\n", "YES"),
    ("I_1406_anagrams", "ananas\nnnaass\n", "NO"),
    ("J_411_max_number", "2\n20\n004\n66\n", "66220004"),
    ("J_411_max_number", "3\n", "3"),
    ("L_111162_taxi", "10 20 30\n50 20 30\n", "1700"),
]

# Максимум сравнений паскалевского QSort, найденный полным перебором.
ANTI_QUICKSORT_MAX = {1: 2, 2: 3, 3: 6, 4: 12, 5: 19, 6: 27,
                      7: 36, 8: 46, 9: 57, 10: 69}


def run(stem, data):
    exe = os.path.join(HERE, stem + ".exe")
    src = os.path.join(HERE, stem + ".py")
    cmd = [exe] if os.path.exists(exe) else [sys.executable, src]
    p = subprocess.run(cmd, input=data.encode(), capture_output=True, timeout=60)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.decode("utf-8", "replace")[:300])
    return p.stdout.decode("utf-8", "replace")


def count_comparisons(a):
    """Счётчик сравнений ровно по псевдокоду из условия задачи 665."""
    a = list(a)
    total = 0
    stack = [(0, len(a) - 1)]
    while stack:
        lo, hi = stack.pop()
        key = a[(lo + hi) // 2]
        i, j = lo, hi
        while True:
            while True:
                total += 1
                if a[i] < key:
                    i += 1
                else:
                    break
            while True:
                total += 1
                if key < a[j]:
                    j -= 1
                else:
                    break
            if i <= j:
                a[i], a[j] = a[j], a[i]
                i += 1
                j -= 1
            if i > j:
                break
        if lo < j:
            stack.append((lo, j))
        if i < hi:
            stack.append((i, hi))
    return total


def main():
    failed = 0
    for stem, data, want in TESTS:
        got = " ".join(run(stem, data).split())
        ok = got == " ".join(want.split())
        failed += not ok
        print("%-26s %s" % (stem, "OK" if ok else "FAIL: ждали %r, получили %r" % (want, got)))

    for n, want in ANTI_QUICKSORT_MAX.items():
        a = [int(x) for x in run("K_665_anti_quicksort", "%d\n" % n).split()]
        ok = sorted(a) == list(range(1, n + 1)) and count_comparisons(a) == want
        failed += not ok
        print("%-26s n=%-3d %s" % ("K_665_anti_quicksort", n, "OK" if ok else "FAIL"))

    print("\nпровалов:", failed)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
