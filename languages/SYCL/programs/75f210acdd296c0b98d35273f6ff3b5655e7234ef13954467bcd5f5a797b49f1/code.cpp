#include <CL/sycl.hpp>
#include <iostream>
#include <vector>

using namespace cl::sycl;

int main() {
    const int N = 1024;
    std::vector<float> a(N, 1.0f);
    std::vector<float> b(N, 2.0f);
    std::vector<float> c(N, 0.0f);

    queue q;

    {
        buffer<float> buf_a(a.data(), range<1>(N));
        buffer<float> buf_b(b.data(), range<1>(N));
        buffer<float> buf_c(c.data(), range<1>(N));

        q.submit([&](handler& h) {
            auto acc_a = buf_a.get_access<access::mode::read>(h);
            auto acc_b = buf_b.get_access<access::mode::read>(h);
            auto acc_c = buf_c.get_access<access::mode::write>(h);

            h.parallel_for(range<1>(N), [=](id<1> i) {
                acc_c[i] = acc_a[i] + acc_b[i];
            });
        });
    }

    std::cout << "Result: c[0] = " << c[0] << std::endl;
    return 0;
}
