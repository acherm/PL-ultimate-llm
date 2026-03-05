(* Concurrent ML: ping-pong between two threads *)

fun ping (outCh, inCh, n) =
  if n = 0 then ()
  else (
    CML.sync (CML.sendEvt (outCh, "ping"));
    let val msg = CML.sync (CML.recvEvt inCh)
    in
      print ("Received: " ^ msg ^ "\n");
      ping (outCh, inCh, n - 1)
    end
  )

fun pong (inCh, outCh) =
  let val msg = CML.sync (CML.recvEvt inCh)
  in
    print ("Received: " ^ msg ^ "\n");
    CML.sync (CML.sendEvt (outCh, "pong"));
    pong (inCh, outCh)
  end

fun main () =
  let
    val ch1 = CML.channel ()
    val ch2 = CML.channel ()
    val _ = CML.spawn (fn () => pong (ch1, ch2))
  in
    ping (ch1, ch2, 3)
  end

val _ = RunCML.doit (main, NONE)
