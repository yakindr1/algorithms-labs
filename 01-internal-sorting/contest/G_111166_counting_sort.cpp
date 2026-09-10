#include <iostream>
#include <vector>

using namespace std;

const int MAX_VALUE = 100;

void CountSort(vector<int>& a) {
    vector<int> count(MAX_VALUE + 1, 0);
    for (size_t i = 0; i < a.size(); ++i) {
        ++count[a[i]];
    }
    size_t pos = 0;
    for (int value = 0; value <= MAX_VALUE; ++value) {
        for (int c = 0; c < count[value]; ++c) {
            a[pos++] = value;
        }
    }
}

int main() {
    vector<int> a;
    int x;
    while (cin >> x) {
        a.push_back(x);
    }
    CountSort(a);
    for (size_t i = 0; i < a.size(); ++i) {
        cout << a[i] << " ";
    }
    cout << endl;
}
