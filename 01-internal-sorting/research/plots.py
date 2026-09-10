"""Графики по результатам замеров."""

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

import generators
import sorts

PLOT_DIR = Path("plots")

ORDER = ["selection", "bubble_naive", "bubble_flag", "insertion",
         "merge", "quick_mid", "quick_random", "heap", "counting"]

NAMES = {
    "selection": "выбором",
    "bubble_naive": "пузырёк наивный",
    "bubble_flag": "пузырёк с флагом",
    "insertion": "вставками",
    "merge": "слиянием",
    "quick_mid": "быстрая, опорный по середине",
    "quick_random": "быстрая, случайный опорный",
    "heap": "пирамидальная",
    "counting": "подсчётом",
}

PROFILE_NAMES = {
    "random": "случайный",
    "sorted": "отсортированный",
    "reversed": "обратный",
    "nearly_sorted": "почти отсортированный",
    "few_unique": "мало уникальных",
}


def _xticks(ax, sizes):
    ax.set_xticks(list(sizes))
    ax.set_xticklabels([str(v) for v in sizes])
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())


def _order(d):
    return d.assign(_k=d.algorithm.map(ORDER.index)).sort_values(["_k", "n"])


def comparisons_vs_theory(d):
    fig, ax = plt.subplots(figsize=(8, 5))
    q = _order(d[(d.algorithm.isin(sorts.QUADRATIC)) & (d.profile == "reversed")])
    # Выбор, пузырёк с флагом и вставки дают ровно одинаковое число
    # сравнений, поэтому маркеры разного размера вкладываются друг в друга.
    style = {"selection": ("o", 13), "bubble_naive": ("s", 8),
             "bubble_flag": ("^", 9), "insertion": ("D", 5)}
    for name in [a for a in ORDER if a in set(q.algorithm)]:
        g = q[q.algorithm == name]
        marker, size = style[name]
        ax.plot(g.n, g.comparisons, marker=marker, ms=size, ls="-", lw=1,
                alpha=.85, label=NAMES[name])
    n = sorted(q.n.unique())
    ax.plot(n, [x * (x - 1) for x in n], "k--", lw=1, label="N(N−1)")
    ax.plot(n, [x * (x - 1) / 2 for x in n], "k:", lw=1.2, label="N(N−1)/2")
    ax.set(xscale="log", yscale="log", xlabel="N", ylabel="сравнений",
           title="Квадратичные сортировки на обратно отсортированном массиве")
    _xticks(ax, n)
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(alpha=.3, which="major")
    ax.set_axisbelow(True)
    fig.savefig(PLOT_DIR / "comparisons_vs_theory.png", dpi=140,
                bbox_inches="tight")
    plt.close(fig)


def time_vs_n(d):
    fig, ax = plt.subplots(figsize=(9, 5))
    q = _order(d[d.profile == "random"])
    for name in ORDER:
        g = q[q.algorithm == name]
        style = "o--" if name in sorts.QUADRATIC else "o-"
        ax.plot(g.n, g.seconds, style, label=NAMES[name])
    ax.set(xscale="log", yscale="log", xlabel="N", ylabel="секунд",
           title="Время работы на случайных данных (пунктир — квадратичные)")
    _xticks(ax, sorted(q.n.unique()))
    ax.legend(fontsize=8, loc="center left", bbox_to_anchor=(1.01, .5),
              frameon=False)
    ax.grid(alpha=.3, which="major")
    ax.set_axisbelow(True)
    fig.savefig(PLOT_DIR / "time_vs_n.png", dpi=140, bbox_inches="tight")
    plt.close(fig)


def profiles_at_n(d, n=1000):
    q = d[d.n == n].pivot_table(index="algorithm", columns="profile",
                                values="comparisons")
    q = q.reindex(ORDER)[list(generators.PROFILES)]
    q.index = [NAMES[a] for a in q.index]
    q.columns = [PROFILE_NAMES[c] for c in q.columns]

    fig, ax = plt.subplots(figsize=(11, 5))
    q.plot.bar(ax=ax, logy=True, width=.82)
    ax.set_ylim(bottom=100)
    ax.set(ylabel="сравнений", xlabel="")
    ax.set_title(f"Зависимость числа сравнений от вида входных данных, N={n}",
                 pad=32)
    ax.grid(alpha=.3, axis="y", which="major")
    ax.set_axisbelow(True)
    ax.legend(fontsize=8, ncol=5, loc="lower center",
              bbox_to_anchor=(.5, 1.01), frameon=False)
    ax.tick_params(axis="x", rotation=25)
    for lbl in ax.get_xticklabels():
        lbl.set_ha("right")

    # Сортировка подсчётом не делает сравнений вообще, на логарифмической
    # шкале её столбцы пропадают — подписываем явно.
    x = list(q.index).index(NAMES["counting"])
    ax.annotate("0 сравнений", xy=(x, 130), ha="center", fontsize=8, rotation=90)
    fig.savefig(PLOT_DIR / "profiles.png", dpi=140, bbox_inches="tight")
    plt.close(fig)


def anti_quicksort_plot(sizes=(200, 500, 1000, 2000, 4000)):
    rows = []
    for n in sizes:
        for label, data in (("случайный вход", generators.make("random", n, seed=7)),
                            ("анти-тест", generators.anti_quicksort(n))):
            st = sorts.new_stats()
            sorts.quick_sort_mid(data, st)
            rows.append((n, label, st[sorts.CMP]))
    d = pd.DataFrame(rows, columns=["n", "вход", "comparisons"])

    fig, ax = plt.subplots(figsize=(8, 5))
    for label, g in d.groupby("вход"):
        ax.plot(g.n, g.comparisons, "o-", label=label)
    n = list(sizes)
    ax.plot(n, [x * x / 2 for x in n], "k--", lw=1, label="N²/2")
    ax.plot(n, [x * 1.39 * (x.bit_length()) for x in n], "k:", lw=1,
            label="≈ N·log₂N")
    ax.set(xscale="log", yscale="log", xlabel="N", ylabel="сравнений",
           title="Быстрая сортировка с опорным по середине на анти-тесте")
    _xticks(ax, n)
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(alpha=.3, which="major")
    ax.set_axisbelow(True)
    fig.savefig(PLOT_DIR / "anti_quicksort.png", dpi=140, bbox_inches="tight")
    plt.close(fig)
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="results.csv")
    args = ap.parse_args()
    PLOT_DIR.mkdir(exist_ok=True)
    d = pd.read_csv(args.csv)
    comparisons_vs_theory(d)
    time_vs_n(d)
    profiles_at_n(d)
    print(anti_quicksort_plot().to_string(index=False))
    print("графики в", PLOT_DIR.resolve())


if __name__ == "__main__":
    main()
