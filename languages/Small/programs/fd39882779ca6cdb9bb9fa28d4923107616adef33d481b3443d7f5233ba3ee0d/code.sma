main()
{
    new a = 0, b = 1, c;
    printf("Fibonacci sequence:\n");
    for (new i = 0; i < 10; i++)
    {
        printf("%d\n", a);
        c = a + b;
        a = b;
        b = c;
    }
}
