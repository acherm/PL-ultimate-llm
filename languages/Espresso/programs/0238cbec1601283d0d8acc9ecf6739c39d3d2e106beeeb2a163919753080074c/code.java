public class Fibonacci {
    public static int fib(int n) {
        if (n <= 1) return n;
        return fib(n - 1) + fib(n - 2);
    }

    public static void main(String[] args) {
        System.out.println("Fibonacci sequence (first 10 terms):");
        for (int i = 0; i < 10; i++) {
            System.out.println("fib(" + i + ") = " + fib(i));
        }
    }
}
