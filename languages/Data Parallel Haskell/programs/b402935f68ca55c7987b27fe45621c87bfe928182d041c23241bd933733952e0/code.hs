{-# LANGUAGE ParallelArrays #-}
{-# OPTIONS_GHC -fvectorise #-}
module DotProduct where

import Data.Array.Parallel
import Data.Array.Parallel.Prelude
import Data.Array.Parallel.Prelude.Double as D

dotp :: [:Double:] -> [:Double:] -> Double
dotp xs ys = D.sumP (zipWithP (*) xs ys)

mapP2 :: (Double -> Double) -> [:Double:] -> [:Double:]
mapP2 f xs = [: f x | x <- xs :]

scaleP :: Double -> [:Double:] -> [:Double:]
scaleP s xs = mapP2 (* s) xs
