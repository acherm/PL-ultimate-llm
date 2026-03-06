// counter.flux -- OFlux example: sequential node pipeline
// OFlux is a flow-based concurrent programming language

node Start (detached)
  guard Nothing ()
  return ( Out int n )
end

node Double
  guard Nothing ()
  param ( In int n )
  return ( Out int result )
end

node Print
  guard Nothing ()
  param ( In int result )
  return ( Done )
end

// Flow definition: wire the nodes together
Initial : Start
Start -> Double
Double -> Print
