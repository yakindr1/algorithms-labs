import sys


def main():
    lines = sys.stdin.read().splitlines()
    distances = [int(x) for x in lines[0].split()]
    tariffs = [int(x) for x in lines[1].split()]

    # Неравенство о перестановках: сумма попарных произведений минимальна,
    # когда один набор возрастает, а другой убывает.
    distances.sort()
    tariffs.sort(reverse=True)

    print(sum(d * t for d, t in zip(distances, tariffs)))


main()
