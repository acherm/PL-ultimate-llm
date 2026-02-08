import extensions;

public program()
{
    int n := 10;
    int a := 0;
    int b := 1;

    for (int i := 0; i < n; i += 1)
    {
        console.printLine(a);
        int temp := a;
        a := b;
        b := temp + b;
    }
}
