import static edu.rice.hj.Module1.*;
import static edu.rice.hj.Module0.*;

/**
 * Parallel Fibonacci using Habanero Java async/finish.
 */
public class Fibonacci {

    static int fib(final int n) {
        if (n <= 1) {
            return n;
        }
        final int[] a = new int[1];
        final int[] b = new int[1];
        finish(() -> {
            async(() -> {
                a[0] = fib(n - 1);
            });
            b[0] = fib(n - 2);
        });
        return a[0] + b[0];
    }

    public static void main(final String[] args) {
        launchHabaneroApp(() -> {
            final int n = Integer.parseInt(args.length > 0 ? args[0] : "10");
            System.out.println("fib(" + n + ") = " + fib(n));
        });
    }
}
