import sys


def merge_sort(a):
    """Восходящее слияние: рекурсия на 10^5 элементов в Python заметно медленнее."""
    n = len(a)
    buf = [0] * n
    width = 1
    while width < n:
        for lo in range(0, n, 2 * width):
            mid = min(lo + width, n)
            hi = min(lo + 2 * width, n)
            i, j, k = lo, mid, lo
            while i < mid and j < hi:
                if a[j] < a[i]:
                    buf[k] = a[j]
                    j += 1
                else:
                    buf[k] = a[i]
                    i += 1
                k += 1
            while i < mid:
                buf[k] = a[i]
                i += 1
                k += 1
            while j < hi:
                buf[k] = a[j]
                j += 1
                k += 1
        a, buf = buf, a
        width *= 2
    return a


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    sys.stdout.write(" ".join(map(str, merge_sort(a))))


main()
