(* Producer-Consumer using CML channels *)
(* Based on examples from John Reppy's Concurrent Programming in ML *)

structure ProducerConsumer =
struct
  open CML

  fun producer (ch, items) =
    let
      fun loop [] = ()
        | loop (x :: xs) =
            ( send (ch, SOME x)
            ; loop xs
            )
    in
      loop items;
      send (ch, NONE)
    end

  fun consumer ch =
    let
      fun loop acc =
        case recv ch of
            NONE => rev acc
          | SOME x => loop (x :: acc)
    in
      loop []
    end

  fun run items =
    let
      val ch : int option chan = channel ()
      val resultEvt = spawn (fn () => producer (ch, items))
      val result = consumer ch
    in
      List.app (fn x => print (Int.toString x ^ " ")) result;
      print "\n"
    end
end

val _ = RunCML.doit (fn () =>
  ProducerConsumer.run [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
  NONE
)