task class FibTask extends Task<Integer, Long> {
    public Long execute(Integer n) {
        if (n <= 1) return (long) n;
        long a = 0, b = 1;
        for (int i = 2; i <= n; i++) {
            long c = a + b;
            a = b;
            b = c;
        }
        return b;
    }
}

public class FibMain {
    public static void main(String[] args) {
        FibTask fib = new FibTask();
        for (int i = 0; i <= 10; i++) {
            System.out.println("fib(" + i + ") = " + fib.execute(i));
        }
    }
}
