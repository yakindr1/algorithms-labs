"""Профили входных данных для замеров."""

import random

PROFILES = ("random", "sorted", "reversed", "nearly_sorted", "few_unique")


def make(profile, n, seed=0, hi=10_000):
    rnd = random.Random(seed)
    if profile == "random":
        return [rnd.randint(0, hi) for _ in range(n)]
    if profile == "sorted":
        return sorted(rnd.randint(0, hi) for _ in range(n))
    if profile == "reversed":
        return sorted((rnd.randint(0, hi) for _ in range(n)), reverse=True)
    if profile == "nearly_sorted":
        a = sorted(rnd.randint(0, hi) for _ in range(n))
        for _ in range(max(1, n // 100)):
            i, j = rnd.randrange(n), rnd.randrange(n)
            a[i], a[j] = a[j], a[i]
        return a
    if profile == "few_unique":
        return [rnd.randint(0, 9) for _ in range(n)]
    raise ValueError("неизвестный профиль: %s" % profile)


def anti_quicksort(n):
    """Перестановка 1..n, на которой опорный по середине даёт худший случай.

    Строится обратным ходом: гоняем сортировку по массиву-заготовке и
    каждый раз ставим текущий опорный элемент на своё минимальное место.
    """
    a = list(range(1, n + 1))
    pos = list(range(n))
    nxt = 1
    stack = [(0, n - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo >= hi:
            continue
        mid = (lo + hi) // 2
        a[pos[mid]] = nxt
        nxt += 1
        pos[mid], pos[lo] = pos[lo], pos[mid]
        stack.append((lo + 1, hi))
    for i in range(n):
        if a[pos[i]] == 0:
            a[pos[i]] = nxt
            nxt += 1
    return a
