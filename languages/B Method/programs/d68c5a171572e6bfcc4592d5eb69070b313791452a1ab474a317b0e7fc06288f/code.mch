MACHINE Counter
VARIABLES cc
INVARIANT cc : NAT
INITIALISATION cc := 0
OPERATIONS
    Increment = PRE cc < MAXINT THEN cc := cc + 1 END;
    Decrement = PRE cc > 0 THEN cc := cc - 1 END;
    val <-- Value = val := cc
END
