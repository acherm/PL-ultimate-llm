module MAC where

import Clash.Prelude

mac :: (HiddenClockResetEnable dom)
    => Signal dom (Signed 9)
    -> Signal dom (Signed 9)
    -> Signal dom (Signed 9)
mac x y = acc
  where
    acc = register 0 (acc + x * y)

topEntity
  :: Clock System
  -> Reset System
  -> Enable System
  -> Signal System (Signed 9)
  -> Signal System (Signed 9)
  -> Signal System (Signed 9)
topEntity = exposeClockResetEnable mac
