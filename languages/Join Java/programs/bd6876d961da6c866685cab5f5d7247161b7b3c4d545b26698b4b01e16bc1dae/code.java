// One-place buffer using Join Java join patterns
// Classic example from the Join Java technical report
class OneBuffer {
    public synchronized String get() & public synchronized void put(String x) {
        return x;
    }
}

public class HelloJoin {
    public static void main(String[] args) throws Throwable {
        OneBuffer buf = new OneBuffer();
        buf.put("Hello, World!");
        System.out.println(buf.get());
        buf.put("Join patterns work!");
        System.out.println(buf.get());
    }
}
