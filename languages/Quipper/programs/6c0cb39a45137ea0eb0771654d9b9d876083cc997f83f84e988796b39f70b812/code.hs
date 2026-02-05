-- Deutsch-Jozsa Algorithm in Quipper
-- Determines whether a boolean function is constant or balanced

import Quipper

-- Oracle function for the algorithm
oracle :: Qubit -> Qubit -> Qubit -> Circ (Qubit, Qubit, Qubit)
oracle x y z = do
  qnot_at z `controlled` [x, y]
  return (x,y,z)

-- Main Deutsch-Jozsa algorithm
deutschjozsa :: (Qubit -> Qubit -> Qubit -> Circ (Qubit, Qubit, Qubit))
                -> Circ (Bit, Bit)
deutschjozsa oracle = do
  x <- qinit False
  y <- qinit False
  z <- qinit True
  hadamard x
  hadamard y
  hadamard z
  (x,y,z) <- oracle x y z
  hadamard x
  hadamard y
  (a,b) <- measure (x,y)
  return (a,b)

-- Run the algorithm
main :: IO ()
main = do
  print_simple Preview (deutschjozsa oracle)