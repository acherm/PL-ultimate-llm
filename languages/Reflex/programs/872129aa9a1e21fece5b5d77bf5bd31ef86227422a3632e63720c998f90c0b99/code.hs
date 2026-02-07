-- A simple counter example in Reflex
import Reflex.Dom

main :: IO ()
main = mainWidget $ el "div" $ do
  el "h1" $ text "Counter Example"
  rec
    let increment = (+1) <$ buttonClick
        decrement = subtract 1 <$ decrementClick
    count <- foldDyn ($) (0 :: Int) $ leftmost [increment, decrement]
    el "div" $ dynText $ fmap (("Count: " ++) . show) count
    buttonClick <- button "Increment"
    decrementClick <- button "Decrement"
  return ()
