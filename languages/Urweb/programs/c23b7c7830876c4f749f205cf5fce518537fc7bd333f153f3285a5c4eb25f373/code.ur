structure Counter = struct
  open Top

  fun main () : unit = let
    val counter = source 0
  in
    return <html><body>
      <dyn signal={n <- signal counter;
                   return <span>{[n]}</span>}/>
      <button onclick={fn _ =>
                       n <- get counter;
                       set counter (n + 1)}>
        Increment
      </button>
    </body></html>
  end
end