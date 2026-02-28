import Control.Concurrent
import Control.Concurrent.MVar
import Control.Concurrent.Chan

-- Simple concurrent logger: multiple worker threads send messages via a shared channel

logger :: Chan String -> MVar () -> IO ()
logger chan done = do
  msg <- readChan chan
  putStrLn msg
  if msg == "STOP"
    then putMVar done ()
    else logger chan done

worker :: Chan String -> Int -> IO ()
worker chan wid = do
  threadDelay (wid * 200000)
  writeChan chan ("Worker " ++ show wid ++ " done after " ++ show wid ++ "00ms")

main :: IO ()
main = do
  chan <- newChan
  done <- newEmptyMVar
  let numWorkers = 4
  mapM_ (\i -> forkIO (worker chan i)) [1..numWorkers]
  forkIO (logger chan done)
  threadDelay 1200000
  writeChan chan "STOP"
  takeMVar done
  putStrLn "All workers finished."
