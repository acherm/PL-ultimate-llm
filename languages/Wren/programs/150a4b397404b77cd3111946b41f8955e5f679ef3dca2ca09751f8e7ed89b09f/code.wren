class Life {
  construct new() {
    _width = 80
    _height = 40
    _cells = List.filled(_width * _height, false)

    // Add a glider.
    this[2, 0] = true
    this[2, 1] = true
    this[2, 2] = true
    this[1, 2] = true
    this[0, 1] = true
  }

  [x, y] { _cells[y * _width + x] }
  [x, y]=(value) { _cells[y * _width + x] = value }

  neighbors(x, y) {
    var count = 0
    for (y1 in (y - 1)..(y + 1)) {
      for (x1 in (x - 1)..(x + 1)) {
        if (x1 == x && y1 == y) continue

        var x2 = x1
        if (x2 < 0) x2 = _width - 1
        if (x2 >= _width) x2 = 0

        var y2 = y1
        if (y2 < 0) y2 = _height - 1
        if (y2 >= _height) y2 = 0

        if (this[x2, y2]) count = count + 1
      }
    }
    return count
  }

  step() {
    var new = List.filled(_width * _height, false)

    for (y in 0..._height) {
      for (x in 0..._width) {
        var n = neighbors(x, y)
        var value = this[x, y]
        new[y * _width + x] = (value && n >= 2 && n <= 3) ||
            (!value && n == 3)
      }
    }

    _cells = new
  }

  toString {
    var result = ""
    for (y in 0..._height) {
      for (x in 0..._width) {
        result = result + (this[x, y] ? "█" : " ")
      }
      result = result + "\n"
    }
    return result
  }
}
