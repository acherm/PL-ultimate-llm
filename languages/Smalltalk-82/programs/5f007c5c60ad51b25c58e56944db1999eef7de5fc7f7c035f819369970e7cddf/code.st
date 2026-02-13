Integer extend [
    factorial [
        self <= 0 ifTrue: [^1].
        ^self * (self - 1) factorial
    ]
]

Transcript show: '5 factorial = ', 5 factorial printString; cr.
