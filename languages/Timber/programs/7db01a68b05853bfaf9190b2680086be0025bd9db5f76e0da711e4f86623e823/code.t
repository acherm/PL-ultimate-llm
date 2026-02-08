module Main where

import POSIX

-- Simple blink program that toggles an LED
blink :: Time -> Action
blink period = do
    led <- new False
    after period $ forever $ do
        old <- get led
        set led (not old)
        after period $ return ()

-- Main entry point
root :: RootAction
root = do
    blink (sec 1)
