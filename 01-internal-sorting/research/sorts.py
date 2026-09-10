"""Сортировки со счётчиками сравнений и присваиваний.

Счётчик — список из двух чисел [сравнения, присваивания].
Обмен двух элементов считается за три присваивания, как в лекции.
"""

CMP = 0
ASG = 1


def new_stats():
    return [0, 0]


def selection_sort(a, st):
    n = len(a)
    for i in range(n - 1):
        m = i
        for j in range(i + 1, n):
            st[CMP] += 1
            if a[j] < a[m]:
                m = j
                st[ASG] += 1
        if m != i:
            a[i], a[m] = a[m], a[i]
            st[ASG] += 3
    return a


def bubble_sort_naive(a, st):
    """Без флага и без сокращения внутреннего цикла: ровно N(N-1) сравнений."""
    n = len(a)
    for _ in range(n):
        for j in range(n - 1):
            st[CMP] += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                st[ASG] += 3
    return a


def bubble_sort_flag(a, st):
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            st[CMP] += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                st[ASG] += 3
                swapped = True
        if not swapped:
            break
    return a


def insertion_sort(a, st):
    for i in range(1, len(a)):
        key = a[i]
        st[ASG] += 1
        j = i - 1
        while j >= 0:
            st[CMP] += 1
            if a[j] <= key:
                break
            a[j + 1] = a[j]
            st[ASG] += 1
            j -= 1
        a[j + 1] = key
        st[ASG] += 1
    return a


def merge_sort(a, st):
    buf = [0] * len(a)
    _merge_sort(a, buf, 0, len(a), st)
    return a


def _merge_sort(a, buf, lo, hi, st):
    if hi - lo <= 1:
        return
    mid = (lo + hi) // 2
    _merge_sort(a, buf, lo, mid, st)
    _merge_sort(a, buf, mid, hi, st)
    i, j, k = lo, mid, lo
    while i < mid and j < hi:
        st[CMP] += 1
        if a[j] < a[i]:
            buf[k] = a[j]
            j += 1
        else:
            buf[k] = a[i]
            i += 1
        st[ASG] += 1
        k += 1
    while i < mid:
        buf[k] = a[i]
        i += 1
        k += 1
        st[ASG] += 1
    while j < hi:
        buf[k] = a[j]
        j += 1
        k += 1
        st[ASG] += 1
    a[lo:hi] = buf[lo:hi]
    st[ASG] += hi - lo


def _quick_sort(a, st, pick_pivot):
    """Разбиение Хоара, как в коде из задачи H («Анти-QuickSort»).

    Стек вместо рекурсии, чтобы вырожденные входы не упирались
    в лимит глубины рекурсии Python.
    """
    stack = [(0, len(a) - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo >= hi:
            continue
        key = a[pick_pivot(lo, hi)]
        i, j = lo, hi
        while i <= j:
            while True:
                st[CMP] += 1
                if a[i] < key:
                    i += 1
                else:
                    break
            while True:
                st[CMP] += 1
                if key < a[j]:
                    j -= 1
                else:
                    break
            if i <= j:
                a[i], a[j] = a[j], a[i]
                st[ASG] += 3
                i += 1
                j -= 1
        if lo < j:
            stack.append((lo, j))
        if i < hi:
            stack.append((i, hi))
    return a


def quick_sort_mid(a, st):
    return _quick_sort(a, st, lambda lo, hi: (lo + hi) // 2)


def quick_sort_random(a, st, rnd=None):
    import random
    r = rnd or random.Random(0)
    return _quick_sort(a, st, lambda lo, hi: r.randint(lo, hi))


def _sift_down(a, i, n, st):
    while True:
        left, right, m = 2 * i + 1, 2 * i + 2, i
        if left < n:
            st[CMP] += 1
            if a[left] > a[m]:
                m = left
        if right < n:
            st[CMP] += 1
            if a[right] > a[m]:
                m = right
        if m == i:
            return
        a[i], a[m] = a[m], a[i]
        st[ASG] += 3
        i = m


def heap_sort(a, st):
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):
        _sift_down(a, i, n, st)
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        st[ASG] += 3
        _sift_down(a, 0, end, st)
    return a


def counting_sort(a, st):
    if not a:
        return a
    lo, hi = min(a), max(a)
    m = hi - lo + 1
    cnt = [0] * m
    st[ASG] += m
    for x in a:
        cnt[x - lo] += 1
        st[ASG] += 1
    k = 0
    for v in range(m):
        c = cnt[v]
        while c:
            a[k] = v + lo
            st[ASG] += 1
            k += 1
            c -= 1
    return a


ALGORITHMS = {
    "selection": selection_sort,
    "bubble_naive": bubble_sort_naive,
    "bubble_flag": bubble_sort_flag,
    "insertion": insertion_sort,
    "merge": merge_sort,
    "quick_mid": quick_sort_mid,
    "quick_random": quick_sort_random,
    "heap": heap_sort,
    "counting": counting_sort,
}

QUADRATIC = {"selection", "bubble_naive", "bubble_flag", "insertion"}
