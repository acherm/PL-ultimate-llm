void VectorAdd(input int<32> a[1024], input int<32> b[1024],
                output int<32> c[1024])
{
    for (int i = 0; i < 1024; i++)
    {
        c[i] = a[i] + b[i];
    }
}
