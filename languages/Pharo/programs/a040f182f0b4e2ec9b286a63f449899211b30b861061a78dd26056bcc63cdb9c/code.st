Object subclass: #Cell
  instanceVariableNames: 'isAlive position neighbors'
  classVariableNames: ''
  package: 'GameOfLife'

Cell>>initialize
  super initialize.
  isAlive := false.
  neighbors := Set new.
  position := 0@0.

Cell>>isAlive
  ^ isAlive

Cell>>isAlive: aBoolean
  isAlive := aBoolean

Cell>>position: aPoint
  position := aPoint

Cell>>addNeighbor: aCell
  neighbors add: aCell

Cell>>nextGeneration
  | livingNeighbors |
  livingNeighbors := (neighbors select: #isAlive) size.
  self isAlive
    ifTrue: [ ^ livingNeighbors = 2 or: [ livingNeighbors = 3 ] ]
    ifFalse: [ ^ livingNeighbors = 3 ]