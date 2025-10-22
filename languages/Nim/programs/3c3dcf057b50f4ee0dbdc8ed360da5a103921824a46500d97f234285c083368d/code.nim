import asyncdispatch, jester

routes:
  get "/":
    resp "Hello World!"

runForever()