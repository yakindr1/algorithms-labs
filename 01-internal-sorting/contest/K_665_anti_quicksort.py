import sys


def anti_quicksort(n):
    """Перестановка 1..n, на которой QuickSort с опорным по середине
    делает максимум сравнений.

    База — известная конструкция обменом a[i] с a[(i+1)//2]. Она отстаёт
    от максимума ровно на одно сравнение при любом n, и обмен значений
    1 и 3 это добирает. Совпадение с полным перебором проверено до n = 10.
    """
    if n == 2:
        return [1, 2]

    a = list(range(1, n + 1))
    for i in range(2, n + 1):
        k = (i + 1) // 2
        a[i - 1], a[k - 1] = a[k - 1], a[i - 1]

    if n >= 3:
        p1, p3 = a.index(1), a.index(3)
        a[p1], a[p3] = a[p3], a[p1]
    return a


def main():
    n = int(sys.stdin.read().split()[0])
    sys.stdout.write(" ".join(map(str, anti_quicksort(n))))


main()
