_Coroutine Fibonacci {
    int fn, fn1, fn2;
  public:
    int next() {
        suspend();
        return fn;
    }
  private:
    void main() {
        fn = 0; fn1 = fn;
        suspend();
        fn = 1; fn2 = fn1; fn1 = fn;
        suspend();
        for ( ;; ) {
            fn = fn1 + fn2; fn2 = fn1; fn1 = fn;
            suspend();
        }
    }
  public:
    Fibonacci() { resume(); }
};

#include <iostream>
using namespace std;

int main() {
    Fibonacci f;
    for ( int i = 1; i <= 10; i += 1 ) {
        cout << f.next() << " ";
    }
    cout << endl;
}