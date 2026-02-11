package life

class Cell {
  var _alive : boolean
  var _nextState : boolean
  var _x : int
  var _y : int
  
  construct(x : int, y : int) {
    _x = x
    _y = y
  }
  
  property get X() : int {
    return _x
  }
  
  property get Y() : int {
    return _y
  }
  
  property get Alive() : boolean {
    return _alive
  }
  
  property set Alive(b : boolean) {
    _alive = b
  }
  
  function calculateNextState(neighbors : List<Cell>) {
    var livingNeighbors = neighbors.countWhere(\n -> n.Alive)
    if(Alive) {
      _nextState = livingNeighbors == 2 || livingNeighbors == 3
    } else {
      _nextState = livingNeighbors == 3
    }
  }
  
  function transition() {
    _alive = _nextState
  }
}