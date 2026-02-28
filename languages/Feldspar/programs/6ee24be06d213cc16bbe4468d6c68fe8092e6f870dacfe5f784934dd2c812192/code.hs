module Examples where

import Feldspar
import Feldspar.Vector

-- | Dot product of two vectors
dotProd :: Pull DIM1 (Data Float) -> Pull DIM1 (Data Float) -> Data Float
dotProd a b = sum (zipWith (*) a b)

-- | Euclidean norm of a vector
norm :: Pull DIM1 (Data Float) -> Data Float
norm v = sqrt (dotProd v v)

-- | Scale a vector by a scalar factor
scale :: Data Float -> Pull DIM1 (Data Float) -> Pull DIM1 (Data Float)
scale s = map (* s)

-- | Sum of all elements in an integer vector
vectorSum :: Pull DIM1 (Data Int32) -> Data Int32
vectorSum = fold (+) 0
