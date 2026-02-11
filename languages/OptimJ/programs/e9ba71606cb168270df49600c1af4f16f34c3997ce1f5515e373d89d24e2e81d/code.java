import ateji.optimj.*;
import java.util.*;

public class KnapsackProblem {
    public static void main(String[] args) {
        int[] values = {60, 100, 120};
        int[] weights = {10, 20, 30};
        int capacity = 50;
        
        int n = values.length;
        boolean[] selected = new boolean[n];
        
        maximize sum(i -> selected[i] ? values[i] : 0, i in 0..n-1)
        subject to {
            sum(i -> selected[i] ? weights[i] : 0, i in 0..n-1) <= capacity;
            forall(i in 0..n-1) selected[i] in {true, false};
        }
        
        System.out.println("Selected items:");
        int totalValue = 0;
        int totalWeight = 0;
        for (int i = 0; i < n; i++) {
            if (selected[i]) {
                System.out.println("Item " + i + ": value=" + values[i] + ", weight=" + weights[i]);
                totalValue += values[i];
                totalWeight += weights[i];
            }
        }
        System.out.println("Total value: " + totalValue);
        System.out.println("Total weight: " + totalWeight);
    }
}
