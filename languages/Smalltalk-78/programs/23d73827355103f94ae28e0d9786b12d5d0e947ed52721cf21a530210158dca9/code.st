Object subclass: #Point
    instanceVariableNames: 'x y'
    classVariableNames: ''
    poolDictionaries: ''

Point methodsFor: 'accessing'

x
    ^x

y
    ^y

x: aNumber
    x := aNumber

y: aNumber
    y := aNumber

Point methodsFor: 'arithmetic'

+ aPoint
    ^Point new x: (x + aPoint x) y: (y + aPoint y)

- aPoint
    ^Point new x: (x - aPoint x) y: (y - aPoint y)

Point methodsFor: 'comparing'

= aPoint
    ^(x = aPoint x) and: [y = aPoint y]
