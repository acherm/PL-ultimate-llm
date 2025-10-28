/* Copyright 2005-2008, Bluespec, Inc.  All rights reserved. */

package Fifo;

/*
 * This FIFO has the standard FIFO interface.
 *
 * The implementation uses a vector of registers and two pointers
 * to identify the valid region of the vector.
 *
 * This implementation is fully parallel.  It can enq and deq in the
 * same cycle when not empty and not full.
 */

import Vector::*;
import FIFO::*;

// A convenient type for FIFO sizes
typedef 4 Size;
typedef TLog#(Size) Ptr;

// An interface with one method, to read the current count
interface FifoCount;
   method ActionValue#(Bit#(Ptr)) count();
endinterface

// The FIFO module
// It has a FIFO interface and a FifoCount interface
// The FIFO interface is parameterized by the type of data in the FIFO
module mkFifo(FIFO#(Bit#(32)));

   // The state
   Reg#(Bit#(32))     data [valueof(Size)];
   Reg#(Bit#(Ptr))    head <- mkReg(0);
   Reg#(Bit#(Ptr))    tail <- mkReg(0);
   Reg#(Bool)         full <- mkReg(False);

   // The interface methods
   interface FIFO fifo;
      method Action enq(Bit#(32) x);
         data[tail] <= x;
         tail <= tail + 1;
         if (head == tail + 1)
            full <= True;
      endmethod

      method Action deq();
         head <= head + 1;
         full <= False;
      endmethod

      method Bit#(32) first();
         return data[head];
      endmethod

      method notFull = !full;

      method notEmpty = (head != tail) || full;
   endinterface

   // The second interface
   interface FifoCount fcount;
      method ActionValue#(Bit#(Ptr)) count();
         let d = tail - head;
         if (full)
            return fromInteger(valueof(Size));
         else
            return d;
      endmethod
   endinterface

endmodule

endpackage
