import sys
from collections import Counter


def main():
    data = sys.stdin.read().split()
    first, second = data[0], data[1]
    # Сортировка запрещена условием, поэтому сравниваем частоты символов за O(n).
    print("YES" if Counter(first) == Counter(second) else "NO")


main()
