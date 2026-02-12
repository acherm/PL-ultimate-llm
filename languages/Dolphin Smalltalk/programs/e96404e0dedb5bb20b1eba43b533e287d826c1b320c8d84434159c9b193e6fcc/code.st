Object subclass: #Point
    instanceVariableNames: 'x y'
    classVariableNames: ''
    poolDictionaries: ''

!Point methodsFor: 'accessing'!

x
    ^x!

x: aNumber
    x := aNumber!

y
    ^y!

y: aNumber
    y := aNumber! !

!Point methodsFor: 'arithmetic'!

+ aPoint
    ^Point new
        x: self x + aPoint x;
        y: self y + aPoint y;
        yourself!

distanceFrom: aPoint
    | dx dy |
    dx := self x - aPoint x.
    dy := self y - aPoint y.
    ^((dx * dx) + (dy * dy)) sqrt! !

!Point methodsFor: 'printing'!

printString
    ^'(' , self x printString , '@' , self y printString , ')'! !

!Point class methodsFor: 'instance creation'!

x: xValue y: yValue
    ^self new
        x: xValue;
        y: yValue;
        yourself! !
