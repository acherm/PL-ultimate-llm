#!/usr/bin/awk -f
BEGIN{
    FS = ","
    OFS = ":"
}
{if(NR > 1) print $1,$4}