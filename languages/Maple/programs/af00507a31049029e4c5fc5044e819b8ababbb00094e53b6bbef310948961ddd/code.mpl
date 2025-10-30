QuickSort := proc( L :: list )
local n, pivot, less, equal, greater, i ;
n := nops( L ) ;
if n < 2 then
 L
else
pivot := L[ n ] ;
less := select( t -> t < pivot, L ) ;
equal := select( t -> t = pivot, L ) ;
greater := select( t -> t > pivot, L ) ;
[ op( QuickSort( less ) ), op( equal ), op( QuickSort( greater ) ) ] ;
end if ;
end proc ;