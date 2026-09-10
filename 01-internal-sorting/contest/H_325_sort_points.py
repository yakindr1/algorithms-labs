import sys
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int

    def squared_distance(self):
        """Квадрат расстояния: порядок тот же, а вещественных чисел нет."""
        return self.x * self.x + self.y * self.y


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    points = []
    for i in range(n):
        x = int(data[1 + 2 * i])
        y = int(data[2 + 2 * i])
        points.append(Point(x, y))

    points.sort(key=Point.squared_distance)

    for p in points:
        print(p.x, p.y)


main()
