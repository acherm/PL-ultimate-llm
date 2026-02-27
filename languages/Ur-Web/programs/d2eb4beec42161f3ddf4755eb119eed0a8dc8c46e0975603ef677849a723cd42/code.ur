fun fact (n : int) : int =
    if n <= 0 then 1
    else n * fact (n - 1)

fun main () : transaction page =
    return <xml>
      <head><title>Factorial</title></head>
      <body>
        <p>10! = {[fact 10]}</p>
      </body>
    </xml>
