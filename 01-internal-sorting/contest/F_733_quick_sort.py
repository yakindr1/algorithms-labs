import random
import sys


def quick_sort(a):
    """Стек вместо рекурсии и случайный опорный: вырожденные входы не страшны."""
    rnd = random.Random(20260910)
    stack = [(0, len(a) - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo >= hi:
            continue
        key = a[rnd.randint(lo, hi)]
        i, j = lo, hi
        while i <= j:
            while a[i] < key:
                i += 1
            while key < a[j]:
                j -= 1
            if i <= j:
                a[i], a[j] = a[j], a[i]
                i += 1
                j -= 1
        if lo < j:
            stack.append((lo, j))
        if i < hi:
            stack.append((i, hi))
    return a


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    sys.stdout.write(" ".join(map(str, quick_sort(a))))


main()
