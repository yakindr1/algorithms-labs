#include <iostream>
#include <vector>

using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; ++i) {
        cin >> a[i];
    }

    // Число обменов пузырьковой сортировки равно числу инверсий массива.
    // При n <= 1000 прямая симуляция укладывается в миллион операций.
    long long swaps = 0;
    for (int i = 0; i < n - 1; ++i) {
        for (int j = 0; j < n - 1 - i; ++j) {
            if (a[j] > a[j + 1]) {
                swap(a[j], a[j + 1]);
                ++swaps;
            }
        }
    }

    cout << swaps << endl;
}
