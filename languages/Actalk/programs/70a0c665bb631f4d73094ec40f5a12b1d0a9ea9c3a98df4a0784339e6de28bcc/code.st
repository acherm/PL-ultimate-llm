"A simple counter actor in Actalk"
"Jean-Pierre Briot, ECOOP 1989"

ActorBehavior subclass: #Counter
    instanceVariableNames: 'count'
    classVariableNames: ''
    poolDictionaries: ''
    category: 'Actalk'.

Counter class >> new [
    ^super new initialize
]

Counter >> initialize [
    count := 0
]

Counter >> increment [
    count := count + 1
]

Counter >> decrement [
    count := count - 1
]

Counter >> count [
    ^count
]

Counter >> printOn: aStream [
    aStream
        nextPutAll: 'Counter(';
        print: count;
        nextPutAll: ')'
]