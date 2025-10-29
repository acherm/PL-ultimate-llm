class point(x, y) {
    method move (dx, dy) -> done {
        x := x + dx ;
        y := y + dy ;
        true
    }
    method getX -> Integer { x }
    method getY -> Integer { y }
}