package GCD;

interface GCD_IFC;
   method Action start(Bit#(32) a, Bit#(32) b);
   method Bit#(32) result();
   method Bool done();
endinterface

module mkGCD(GCD_IFC);
   Reg#(Bit#(32)) x <- mkReg(0);
   Reg#(Bit#(32)) y <- mkReg(0);

   rule compute (x != 0 && y != 0);
      if (x > y)
         x <= x - y;
      else
         y <= y - x;
   endrule

   method Action start(Bit#(32) a, Bit#(32) b);
      x <= a;
      y <= b;
   endmethod

   method Bit#(32) result();
      return (x != 0) ? x : y;
   endmethod

   method Bool done();
      return (x == 0 || y == 0);
   endmethod
endmodule

endpackage
