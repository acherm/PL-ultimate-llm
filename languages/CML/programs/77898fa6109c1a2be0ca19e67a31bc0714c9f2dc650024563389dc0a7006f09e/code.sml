(* Concurrent Sieve of Eratosthenes in Concurrent ML
 * Demonstrates channel-based concurrency with synchronous events.
 *)
local
  open CML
in

(* Generate integers starting from 'start' on channel outCh *)
fun counter (start, outCh) =
  let
    fun loop n = (sync (sendEvt (outCh, n)); loop (n + 1))
  in
    loop start
  end

(* Filter out multiples of prime from inCh, forwarding rest to outCh *)
fun filter (inCh, outCh, prime) =
  let
    fun loop () =
      let
        val n = sync (recvEvt inCh)
      in
        if n mod prime <> 0
          then sync (sendEvt (outCh, n))
          else ();
        loop ()
      end
  in
    loop ()
  end

(* Print the first 'limit' primes using a concurrent sieve pipeline *)
fun sieve limit =
  let
    val naturals = channel ()
    val _ = spawn (fn () => counter (2, naturals))
    fun loop (inCh, count) =
      if count >= limit
        then ()
        else
          let
            val p = sync (recvEvt inCh)
            val _ = TextIO.print (Int.toString p ^ "\n")
            val outCh = channel ()
            val _ = spawn (fn () => filter (inCh, outCh, p))
          in
            loop (outCh, count + 1)
          end
  in
    loop (naturals, 0)
  end

fun main () = RunCML.doit (fn () => sieve 10, NONE)

end
