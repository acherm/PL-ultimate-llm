/ Quicksort in Q (kdb+)
qsort:{$[1>=count x;x;.z.s[x where x<first x],(x where x=first x),.z.s[x where x>first x]]}

/ Test with numeric list
show qsort 5 3 1 4 1 5 9 2 6 5 3 5

/ Test with symbol list
show qsort `mango`banana`apple`cherry`date
