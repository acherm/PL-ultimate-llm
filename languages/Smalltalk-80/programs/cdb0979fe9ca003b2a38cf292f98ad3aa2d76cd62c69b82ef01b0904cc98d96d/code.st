Object subclass: #Counter
    instanceVariableNames: 'count'
    classVariableNames: ''
    poolDictionaries: ''
    category: 'Examples'

Counter methodsFor: 'initialization'

initialize
    count := 0

Counter methodsFor: 'accessing'

increment
    count := count + 1

decrement
    count := count - 1

value
    ^count
