module Blink where

import Ivory.Language
import Ivory.Stdlib

blink :: Def ('[Ref s (Stored Uint8)] :-> ())
blink = proc "blink" $ \led -> body $ do
  ledVal <- deref led
  ifte_ (ledVal ==? 0)
    (store led 1)
    (store led 0)

main :: Def ('[] :-> ())
main = proc "main" $ body $ do
  led <- local (ival 0)
  forever $ do
    call_ blink led
    delay 1000
  where
    delay :: Uint32 -> Ivory eff ()
    delay n = return ()