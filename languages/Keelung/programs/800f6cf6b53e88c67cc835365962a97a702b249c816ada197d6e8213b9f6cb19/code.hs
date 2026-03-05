import Keelung

-- | A simple adder circuit: asserts that a + b = c
adderCircuit :: Comp ()
adderCircuit = do
  a <- input Public :: Comp Field
  b <- input Public :: Comp Field
  c <- input Public :: Comp Field
  assert (a + b `eq` c)

-- | A multiplier circuit: asserts that a * b = c
multiplierCircuit :: Comp ()
multiplierCircuit = do
  a <- input Public :: Comp Field
  b <- input Public :: Comp Field
  c <- input Public :: Comp Field
  assert (a * b `eq` c)

main :: IO ()
main = do
  putStrLn "Compiling adder circuit..."
  result <- compile GF181 adderCircuit
  case result of
    Left err -> print err
    Right r  -> print r
