variable universe 2000 allot
variable newverse 2000 allot

: xy>offset ( x y -- offset )
  50 * + ;
: offset>xy ( offset -- x y )
  50 /mod ;
: alive? ( offset -- flag )
  universe + c@ ;
: set-cell ( offset -- )
  universe + 1 swap c! ;
: clear-cell ( offset -- )
  universe + 0 swap c! ;

: count-neighbors ( offset -- neighbors )
  0 >r
  offset>xy
  -1 -1 2over + xy>offset alive? r> + >r
   0 -1 2over + xy>offset alive? r> + >r
   1 -1 2over + xy>offset alive? r> + >r
  -1  0 2over + xy>offset alive? r> + >r
   1  0 2over + xy>offset alive? r> + >r
  -1  1 2over + xy>offset alive? r> + >r
   0  1 2over + xy>offset alive? r> + >r
   1  1 2over + xy>offset alive? r> + drop
  2drop ;

: randomize ( -- )
  2000 0 do
    i universe + 2 random c!
  loop ;

: swap-universes ( -- )
  universe @ newverse @ universe ! newverse ! ;

: generation ( -- )
  2000 0 do
    i alive? if
      i count-neighbors
      dup 2 < if
        drop i newverse + 0 swap c!
      else
        dup 3 > if
          drop i newverse + 0 swap c!
        else
          drop i newverse + 1 swap c!
        then
      then
    else
      i count-neighbors 3 = if
        i newverse + 1 swap c!
      else
        i newverse + 0 swap c!
      then
    then
  loop
  swap-universes ;