process spec producer(chan(int) c)
{
    int i;
    for (i = 0; i < 10; i++) {
        c ! i;  /* send i to channel c */
    }
}

process spec consumer(chan(int) c)
{
    int v;
    while (1) {
        c ? v;  /* receive from channel c */
        printf("Received: %d\n", v);
        if (v >= 9) break;
    }
}

process body main()
{
    chan(int) ch = create chan(int, 5);
    process producer(ch);
    process consumer(ch);
}
