qsort:{[x]
  $[0=count x;x;
    x0:first x;
    rest:1_x;
    smaller:rest x0<rest;
    larger:rest x0>=rest;
    (qsort smaller),x0,qsort larger
   ]
  }

q)qsort 3 1 4 1 5 9
1 1 3 4 5 9