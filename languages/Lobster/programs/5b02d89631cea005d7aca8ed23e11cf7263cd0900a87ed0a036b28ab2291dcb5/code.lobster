import vec

let gridsize = 50
let cellsize = 10

class cell:
    alive:bool
    next:bool

let grid = map(gridsize) y: map(gridsize) x: cell { false, false }

def neighbors(x, y):
    return fold(range(-1, 2)) y1, total:
        fold(range(-1, 2)) x1, total:
            if x1 == 0 and y1 == 0: total
            else:
                let xw = (x + x1 + gridsize) % gridsize
                let yw = (y + y1 + gridsize) % gridsize
                total + if grid[yw][xw].alive: 1 else: 0

def step():
    for(grid) y, yv: for(yv) x, c:
        let n = neighbors(x, y)
        c.next = if c.alive:
            n == 2 or n == 3
        else:
            n == 3
    for(grid) y, yv: for(yv) x, c:
        c.alive = c.next