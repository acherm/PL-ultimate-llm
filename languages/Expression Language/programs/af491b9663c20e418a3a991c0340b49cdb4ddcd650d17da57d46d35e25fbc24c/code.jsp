<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html>
<head>
  <title>EL Arithmetic and Logical Demo</title>
</head>
<body>
  <h2>Arithmetic Operations</h2>
  <p>Addition: ${3 + 4}</p>
  <p>Subtraction: ${10 - 3}</p>
  <p>Multiplication: ${5 * 6}</p>
  <p>Division: ${10 div 4}</p>
  <p>Modulus: ${10 mod 3}</p>

  <h2>Logical Operations</h2>
  <p>True AND False: ${true and false}</p>
  <p>NOT False: ${not false}</p>

  <h2>Conditional</h2>
  <p>Larger of 5 and 9: ${5 > 9 ? 5 : 9}</p>

  <h2>Comparison</h2>
  <p>Is 10 equal to 10? ${10 == 10}</p>
  <p>Is 5 greater than 3? ${5 > 3}</p>
</body>
</html>
