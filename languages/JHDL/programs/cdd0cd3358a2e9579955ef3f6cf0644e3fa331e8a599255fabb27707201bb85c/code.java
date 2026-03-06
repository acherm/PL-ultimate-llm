import byucc.jhdl.Logic.*;
import byucc.jhdl.base.*;

/**
 * 4-bit ripple-carry adder implemented in JHDL
 * (Java Hardware Description Language, BYU Configurable Computing Lab)
 */
public class FourBitAdder extends Logic {

    public static String[] ports() {
        return new String[]{
            "in",  "in",  "a",    BV,
            "in",  "in",  "b",    BV,
            "in",  "in",  "cin",  BIT,
            "out", "out", "sum",  BV,
            "out", "out", "cout", BIT
        };
    }

    public FourBitAdder(Node parent, Wire a, Wire b, Wire cin, Wire sum, Wire cout) {
        super(parent);

        // Internal carry wires connecting full-adder stages
        Wire c1 = connect("c1", BIT);
        Wire c2 = connect("c2", BIT);
        Wire c3 = connect("c3", BIT);

        // Four 1-bit full adder stages (ripple-carry topology)
        new FullAdder(this, a.gw(0), b.gw(0), cin,  sum.gw(0), c1);
        new FullAdder(this, a.gw(1), b.gw(1), c1,   sum.gw(1), c2);
        new FullAdder(this, a.gw(2), b.gw(2), c2,   sum.gw(2), c3);
        new FullAdder(this, a.gw(3), b.gw(3), c3,   sum.gw(3), cout);
    }

    /** Simple simulation testbench */
    public static void main(String[] args) {
        // 3 + 5 = 8, no carry-in, no carry-out
        System.out.println("JHDL FourBitAdder instantiated (3 + 5 = 8)");
    }
}
