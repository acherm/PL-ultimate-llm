function fact(uint n) -> (uint r)
ensures r >= 0:
{
    if (n == 0) {
        return 1;
    }
    return n * fact(n - 1);
}