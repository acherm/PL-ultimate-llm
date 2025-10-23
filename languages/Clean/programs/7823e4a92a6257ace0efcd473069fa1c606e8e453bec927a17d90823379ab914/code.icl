module life
import StdEnv, StdArray

:: Cell = Alive | Dead
:: Grid = {Grid :: !u:u:[Cell] !Int !Int}

initGrid :: Int Int -> Grid
initGrid rows cols = {Grid {Dead \ _ <- [1..rows*cols]} rows cols}

setCell :: Int Int Cell Grid -> Grid
setCell row col cell grid
  # (Grid cells r c) = grid
  # idx = row * c + col
  # cells = {cells & [idx] = cell}
  = {Grid cells r c}

countNeighbours :: Int Int Grid -> Int
countNeighbours row col grid
  # (Grid _ r c) = grid
  = sum [isAlive (getCell (row+dr) (col+dc) grid) \ (dr,dc) <- deltas]
  where
    deltas = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    getCell r c g
      | r < 0 || r >= fst3 g || c < 0 || c >= snd3 g = Dead
      | otherwise = thd3 g.[r * snd3 g + c]
    isAlive Alive = 1
    isAlive Dead  = 0
    fst3 (Grid a b c) = b
    snd3 (Grid a b c) = c
    thd3 (Grid a b c) = a

nextGen :: Grid -> Grid
nextGen grid
  # (Grid cells rows cols) = grid
  = foldl (flip (foldl (\g r -> foldl (\gg c -> setCell r c (nextState r c grid) gg) g [0..cols-1]))) 
          {grid & Grid.cells = {cells}}
          [0..rows-1]
  where
    nextState r c g = case (isAlive cells.[r*cols+c], countNeighbours r c g) of
      (True, n) | n < 2 || n > 3 -> Dead
                | otherwise      -> Alive
      (False, 3)                 -> Alive
      _                          -> Dead

isAlive :: Cell -> Bool
isAlive Alive = True
isAlive Dead  = False

toString :: Grid -> [Char]
toString {Grid cells rows cols} = concat [[toChar cells.[r*cols+c] \ c <- [0..cols-1]] ++ "\n" \ r <- [0..rows-1]]
  where
    toChar Alive = '*'
    toChar Dead  = '.'

Start :: *World
Start
  # glider = foldl (\g (r,c) -> setCell r c Alive g) (initGrid 5 5) [(1,2),(2,3),(3,1),(3,2),(3,3)]
  = StdEnv.printn (toString (iterate nextGen glider !! 5))