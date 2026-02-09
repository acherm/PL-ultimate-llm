Integer extend [
    fibonacci [
        | a b |
        a := 0.
        b := 1.
        self timesRepeat: [
            | temp |
            temp := a + b.
            a := b.
            b := temp.
        ].
        ^ a
    ]
]

1 to: 16 do: [:i |
    Transcript show: i printString, ': ', i fibonacci printString; cr.
]
