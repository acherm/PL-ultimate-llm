IsAbelianSquareFree := function( G )
    local   F, n, p;
    # G must be a group
    if not IsGroup( G ) then
        Error( "usage: IsAbelianSquareFree( <group> )" );
    fi;
    # G must be abelian
    if not IsAbelian( G ) then
        return false;
    fi;
    # the order must be squarefree
    n := Order( G );
    F := Factors( n );
    for p in F do
        if n mod (p*p) = 0 then
            return false;
        fi;
    od;
    # otherwise G is an abelian squarefree group
    return true;
end;