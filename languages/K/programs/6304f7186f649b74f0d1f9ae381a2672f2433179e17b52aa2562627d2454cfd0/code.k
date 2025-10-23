/ sudoku solver
/ s is 9x9 integer matrix, 0 for unknown
/ e.g. s:("i";",")0:0: `sudoku.txt
/ solve s
/
b:9 9#til 81            /box
c:9 9#b@;b              /col
r:9 9#b                /row
/
solve:{[s]
 m:s=0;
 cands:m#enlist[1+til 9] except' s[r],s[c],s[b];
 if[~any m;:s];
 i:first where m;
 :first solve'[s,'[;i;]'cands i]
 }