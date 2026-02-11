#!/usr/sbin/dtrace -s

/*
 * syscall_count.d - Count system calls by process name
 * This script counts the number of system calls made by each process.
 */

#pragma D option quiet

dtrace:::BEGIN
{
        printf("Tracing system calls... Hit Ctrl-C to end.\n");
}

syscall:::entry
{
        @calls[execname] = count();
}

dtrace:::END
{
        printf("\n%-32s %s\n", "PROCESS", "COUNT");
        printa("%-32s %@d\n", @calls);
}
