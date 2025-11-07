ForAll( PrimeNumbers,
    If( Value > 1,
        ForAll( Sequence( Value - 2, 2 ),
            If( Mod( Value, Value1 ) = 0,
                Collect( Divisors, Value );
                false
            )
        )
    )
)