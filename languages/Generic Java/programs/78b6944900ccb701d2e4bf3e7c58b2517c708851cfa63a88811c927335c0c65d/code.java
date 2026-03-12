// Generic Java (GJ) - bounded polymorphism example
// Demonstrates parameterized types with the 'implements' bound syntax

interface Comparable<A> {
    public int compareTo(A that);
}

class Min {
    static <A implements Comparable<A>> A min(A x, A y) {
        if (x.compareTo(y) <= 0) return x;
        else return y;
    }
}

class IntPair implements Comparable<IntPair> {
    int x, y;

    IntPair(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public int compareTo(IntPair that) {
        if (this.x != that.x) return this.x - that.x;
        return this.y - that.y;
    }

    public String toString() {
        return "(" + x + ", " + y + ")";
    }
}

class Main {
    public static void main(String[] args) {
        IntPair a = new IntPair(1, 3);
        IntPair b = new IntPair(2, 1);
        IntPair m = Min.min(a, b);
        System.out.println("Min of " + a + " and " + b + " is: " + m);
    }
}
