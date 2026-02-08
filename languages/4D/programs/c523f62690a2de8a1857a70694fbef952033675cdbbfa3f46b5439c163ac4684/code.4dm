// Fibonacci sequence in 4D
// Computes and displays the first 20 Fibonacci numbers

C_LONGINT($i;$n;$a;$b;$temp)
C_TEXT($result)

$n:=20
$a:=0
$b:=1
$result:=""

For ($i;1;$n)
    $result:=$result+String($a)+"\n"
    $temp:=$a+$b
    $a:=$b
    $b:=$temp
End for

ALERT($result)
