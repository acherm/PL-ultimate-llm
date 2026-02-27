"use hiphop"

import * as hh from "@hop/hiphop";

// ABRO: classic reactive benchmark - wait for both A and B, emit C, reset on R
const abro = hiphop module() {
   in A; in B; in R; out C;
   do {
      fork {
         await(A.now);
      } par {
         await(B.now);
      }
      emit C();
   } every(R.now)
}

const machine = new hh.ReactiveMachine(abro, "abro");
machine.addEventListener("C", e => console.log("C emitted!"));

// Test sequence
machine.react({ A: true });   // receive A
machine.react({ B: true });   // receive B -> emits C
machine.react({ R: true });   // reset
machine.react({ A: true });   // receive A again
machine.react({ B: true });   // receive B -> emits C again
