-- FRAN (Functional Reactive Animation) tutorial example
-- Source: https://conal.net/fran/tutorial.htm

module Main where

import Fran

-- A ball whose size wiggles over time
wiggleBall :: ImageB
wiggleBall = stretch (2 + wiggle) (solidEllipse yellow)

-- A ball orbiting in a circle
orbitingBall :: ImageB
orbitingBall =
  move (cos2 1 0 * 2, sin2 1 0 * 2) $
    withColor red (solidCircle 0.3)

-- Combine both animations side by side
combined :: ImageB
combined = wiggleBall `over` orbitingBall

main :: IO ()
main = animate combined
