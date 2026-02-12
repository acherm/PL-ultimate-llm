-- Import Copilot Language
import Copilot.Language
import Copilot.Library.PTLTL
import Copilot.Compile.C99

-- | A simple Copilot program that monitors temperature
spec :: Spec
spec = do
  -- Input stream representing temperature sensor
  let temperature = extern "temperature" Nothing

  -- Output trigger when temperature exceeds threshold
  trigger "overheating" (temperature > 100) []

-- Compile and generate C code
main :: IO ()
main = reify spec >>= compile "temperature_monitor"
