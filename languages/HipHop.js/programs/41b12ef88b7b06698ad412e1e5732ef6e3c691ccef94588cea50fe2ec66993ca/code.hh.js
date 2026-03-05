"use hiphop"

// ABRO: the hello-world of synchronous reactive programming
// Emits O when both A and B have been received; resets on R

hiphop module abro() {
  in A, B, R;
  out O;
  loop {
    fork {
      await (A.now);
    } par {
      await (B.now);
    }
    emit O();
    if (R.now) break;
  }
}
