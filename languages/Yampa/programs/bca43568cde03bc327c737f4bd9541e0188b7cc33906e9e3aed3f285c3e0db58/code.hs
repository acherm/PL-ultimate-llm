import FRP.Yampa

gravity :: Double
gravity = 9.81

-- | Signal function representing a bouncing ball.
-- Input: () (no external input)
-- Output: (position, velocity)
bouncingBall :: Double -> Double -> SF () (Double, Double)
bouncingBall y0 v0 = switch (fallingBall y0 v0) (\(y, _) -> bouncingBall y 0)
  where
    fallingBall :: Double -> Double -> SF () ((Double, Double), Event (Double, Double))
    fallingBall y0 v0 = proc () -> do
      v <- (v0 -) ^<< integral -< gravity
      y <- (y0 +) ^<< integral -< v
      let hit = y <= 0 && v < 0
      returnA -< ((y, v), if hit then Event (0, abs v * 0.8) else NoEvent)

main :: IO ()
main = do
  let dt = 0.05
  embedSynch (bouncingBall 10.0 0.0) (deltaEncode dt (repeat ()))
    >>= mapM_ (\(y, v) -> putStrLn ("y=" ++ show y ++ "  v=" ++ show v))
    . take 40
