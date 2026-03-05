#include <CL/sycl.hpp>
#include <iostream>
#include <vector>
using namespace sycl;

int main() {
    const int N = 256;
    std::vector<int> a(N, 1), b(N, 2), c(N, 0);

    queue q;

    {
        buffer buf_a(a), buf_b(b), buf_c(c);
        q.submit([&](handler &h) {
            auto acc_a = buf_a.get_access<access::mode::read>(h);
            auto acc_b = buf_b.get_access<access::mode::read>(h);
            auto acc_c = buf_c.get_access<access::mode::write>(h);
            h.parallel_for(range<1>(N), [=](id<1> i) {
                acc_c[i] = acc_a[i] + acc_b[i];
            });
        });
    }

    bool correct = true;
    for (int i = 0; i < N; i++) {
        if (c[i] != 3) { correct = false; break; }
    }
    std::cout << (correct ? "Result: Correct" : "Result: Incorrect") << std::endl;
    return 0;
}
