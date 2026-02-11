type color = Red | Green | Blue

let color_to_string = function
  | Red -> "red"
  | Green -> "green"
  | Blue -> "blue"

let main () =
  let c = Red in
  Io.format "Color: ~s~n" [color_to_string c]
