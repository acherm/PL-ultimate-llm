Object subclass: #SimpleExample
	instanceVariableNames: ''
	classVariableNames: ''
	package: 'Etoys-Examples'

SimpleExample>>exampleMethod
	"This is a simple example method in Etoys"
	| sum |
	sum := 0.
	1 to: 10 do: [:i | sum := sum + i].
	^sum