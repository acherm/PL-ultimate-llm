# Simple async file reading with IcedCoffeeScript
fs = require 'fs'

readAndPrint = (filename) ->
  await fs.readFile filename, 'utf8', defer err, data
  if err
    console.log "Error: #{err}"
  else
    console.log "File contents:"
    console.log data

readAndPrint 'example.txt'
