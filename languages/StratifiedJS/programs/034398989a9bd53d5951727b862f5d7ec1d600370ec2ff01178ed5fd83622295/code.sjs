// StratifiedJS: structured concurrency with waitfor/or
// Demonstrates timeout and parallel fetch patterns

var http = require('sjs:http');
var sys = require('sjs:sys');

// Fetch URL with timeout; throws on timeout
function getWithTimeout(url, ms) {
  waitfor {
    return http.get(url);
  } or {
    hold(ms);
    throw new Error('Timeout after ' + ms + 'ms');
  }
}

// Run two requests in parallel, collect both results
function fetchPair(url1, url2) {
  var r1, r2;
  waitfor {
    r1 = http.get(url1);
  } and {
    r2 = http.get(url2);
  }
  return [r1, r2];
}

// Countdown using hold() - suspends execution without blocking
function countdown(n) {
  while (n > 0) {
    sys.puts(n + '...');
    hold(1000);
    n--;
  }
  sys.puts('Done!');
}

countdown(3);
