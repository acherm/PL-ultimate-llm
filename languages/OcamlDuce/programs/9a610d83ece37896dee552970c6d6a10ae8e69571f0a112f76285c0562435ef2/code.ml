(* OcamlDuce example: basic XML type manipulation *)
(* OcamlDuce extends OCaml with CDuce's type-safe XML processing *)

type greeting = {{ <greeting>[PCDATA] }}

let greet (msg : {{ Latin1 }}) : {{ greeting }} =
  {{ <greeting>[msg] }}

let extract (g : {{ greeting }}) : {{ Latin1 }} =
  match g with {{ <greeting>[s] }} -> s

let () =
  let g = greet {{ "Hello, OcamlDuce!" }} in
  let s = extract g in
  print_string (CDuce.string_of_latin1 s);
  print_newline ()
