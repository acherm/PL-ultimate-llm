import java.util.ArrayList;
import java.util.List;

public class Sieve {
    public static void main(String[] args) {
        int limit = 2000000;
        long startTime = System.nanoTime();
        List<Integer> sieve = new ArrayList<>();
        for (int i = 2; i <= limit; i++) {
            sieve.add(i);
        }
        int l = sieve.size();
        for (int i = 0; i < l; i++) {
            int p = sieve.get(i);
            if (p * p > limit) {
                break;
            }
            int j = i + p;
            while (j < l) {
                sieve.remove(j);
                l--;
                j += p;
            }
        }
        long estimatedTime = System.nanoTime() - startTime;
        System.out.println("Elapsed time: " + estimatedTime / 1000000.0 + " milliseconds.");
        System.out.println("Number of primes: " + sieve.size());
    }
}