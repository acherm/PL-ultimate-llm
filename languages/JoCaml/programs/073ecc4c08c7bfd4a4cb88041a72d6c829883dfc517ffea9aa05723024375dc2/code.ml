(* Simple channel communication in JoCaml *)

def put(x) & get() = reply x to get

let sender() =
  for i = 0 to 9 do
    put(i);
    Printf.printf "Sent: %d
" i;
    flush stdout
  done

let receiver() =
  for i = 0 to 9 do
    let value = get() in
    Printf.printf "Received: %d
" value;
    flush stdout
  done

let () =
  spawn sender();
  spawn receiver()
