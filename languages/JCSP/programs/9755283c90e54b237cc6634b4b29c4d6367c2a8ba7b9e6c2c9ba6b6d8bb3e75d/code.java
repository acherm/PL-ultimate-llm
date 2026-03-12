import org.jcsp.lang.*;

/**
 * JCSP producer-consumer example demonstrating CSP channel communication.
 */
public class ProducerConsumer {

    public static void main(final String[] args) {
        final One2OneChannel channel = Channel.one2one();

        final CSProcess producer = new CSProcess() {
            public void run() {
                final ChannelOutput out = channel.out();
                for (int i = 0; i < 5; i++) {
                    out.write(i);
                    System.out.println("Produced: " + i);
                }
                out.write(-1); // poison pill
            }
        };

        final CSProcess consumer = new CSProcess() {
            public void run() {
                final ChannelInput in = channel.in();
                while (true) {
                    final int value = (Integer) in.read();
                    if (value < 0) break;
                    System.out.println("Consumed: " + value);
                }
            }
        };

        new Parallel(new CSProcess[] { producer, consumer }).run();
        System.out.println("Done.");
    }
}
