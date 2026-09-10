#include <iostream>
#include <vector>

using namespace std;

void SelectionSort(vector<int>& a) {
    int n = a.size();
    for (int i = 0; i < n - 1; ++i) {
        int max_pos = i;
        for (int j = i + 1; j < n; ++j) {
            if (a[j] > a[max_pos]) {
                max_pos = j;
            }
        }
        if (max_pos != i) {
            swap(a[i], a[max_pos]);
        }
    }
}

int main() {
    vector<int> a;
    int x;
    while (cin >> x) {
        a.push_back(x);
    }
    SelectionSort(a);
    for (size_t i = 0; i < a.size(); ++i) {
        cout << a[i] << " ";
    }
    cout << endl;
}
