program Fibonacci;
var
    n, i, a, b, temp : integer;
begin
    n := 10;
    a := 0;
    b := 1;
    writeln('Fibonacci sequence:');
    for i := 1 to n do
    begin
        writeln(a);
        temp := a + b;
        a := b;
        b := temp
    end
end.
