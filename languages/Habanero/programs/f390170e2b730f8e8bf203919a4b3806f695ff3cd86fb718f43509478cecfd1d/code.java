import static edu.rice.hj.Module1.*;
import static edu.rice.hj.Module0.*;

public class Fibonacci {
    static int fib(int n) throws SuspendableException {
        if (n <= 1) return n;
        HjFuture<Integer> f1 = future(() -> fib(n - 1));
        int f2 = fib(n - 2);
        return f1.get() + f2;
    }

    public static void main(String[] args) throws SuspendableException {
        launchHabaneroApp(() -> {
            for (int n = 0; n <= 10; n++) {
                final int x = n;
                System.out.println("fib(" + x + ") = " + fib(x));
            }
        });
    }
}
