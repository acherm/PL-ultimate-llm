_agg my_agg;

_probe foo() -> int retval {
    my_agg <<< retval;
}

_probe _timer.s(3) {
    long cnt = _count(my_agg);
    if (cnt == 0) {
        printf("no samples found.\n");
        _exit();
    }
    printf("min/avg/max: %ld/%ld/%ld\n", _min(my_agg), _avg(my_agg), _max(my_agg));
    _print(_hist_log(my_agg));
}
