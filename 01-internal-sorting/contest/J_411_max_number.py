import sys
from functools import cmp_to_key


def compare(x, y):
    """x идёт раньше y, если склейка xy больше склейки yx."""
    if x + y > y + x:
        return -1
    if x + y < y + x:
        return 1
    return 0


def main():
    parts = sys.stdin.read().split()
    parts.sort(key=cmp_to_key(compare))
    sys.stdout.write("".join(parts))


main()
