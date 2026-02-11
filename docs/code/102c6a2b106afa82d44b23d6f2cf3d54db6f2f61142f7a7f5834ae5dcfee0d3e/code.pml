#define N 2
mtype = { join, data, ack };
chan q = [4] of { mtype, byte }; /* a channel with 4 slots */

active proctype Server() {
  byte n; mtype cmd;
  do
  :: q ? cmd, n ->
     if
     :: cmd == join -> printf("S: %d joins the club\n", n)
     :: cmd == data -> printf("S: %d sends data\n", n)
     fi;
     q ! ack, 0
  od
}

active [N] proctype Client() {
  byte me = _pid; /* my own process id */
  q ! join, me;
  q ? ack, -;
  q ! data, me;
  q ? ack, -
}