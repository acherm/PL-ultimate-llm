-- Atom: A domain-specific language for embedded hard real-time programming
-- Simple counter and LED blinker examples
module Main where

import Language.Atom

-- | A simple counter that increments each clock period
counterSpec :: Atom ()
counterSpec = atom "counter" $ do
  cnt <- word32 "count" 0
  atom "increment" $
    cnt <== value cnt + 1

-- | LED blinker: toggles every 500 clock periods
blinkerSpec :: Atom ()
blinkerSpec = atom "blinker" $ do
  led <- bool "led" False
  period 1000 $ exactPhase 0   $ atom "led_on"  $ led <== true
  period 1000 $ exactPhase 500 $ atom "led_off" $ led <== false

main :: IO ()
main = do
  compile "counter" defaults counterSpec
  compile "blinker" defaults blinkerSpec
