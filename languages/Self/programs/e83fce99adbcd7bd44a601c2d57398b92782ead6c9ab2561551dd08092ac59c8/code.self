(|
    hanoi = (|
        parent* = traits clonable.
        
        move: disc from: from to: to using: using = (
            disc > 1 ifTrue: [
                self move: disc - 1 from: from to: using using: to.
            ].
            ('Move disk ', disc, ' from ', from, ' to ', to) printLine.
            disc > 1 ifTrue: [
                self move: disc - 1 from: using to: to using: from.
            ].
        ).
    |).
    
    hanoi move: 4 from: 'A' to: 'C' using: 'B'.
|)