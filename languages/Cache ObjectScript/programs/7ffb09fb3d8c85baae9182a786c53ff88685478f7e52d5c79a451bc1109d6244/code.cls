Class MyApp.Fibonacci Extends %RegisteredObject
{

ClassMethod Run()
{
    Write "Fibonacci sequence (first 15 terms):",!
    Set a = 0, b = 1
    Write a,!
    For i = 1:1:14 {
        Write b,!
        Set temp = a + b
        Set a = b
        Set b = temp
    }
}

ClassMethod FibN(n As %Integer) As %Integer
{
    If n = 0 { Return 0 }
    If n = 1 { Return 1 }
    Return ..FibN(n-1) + ..FibN(n-2)
}

}
