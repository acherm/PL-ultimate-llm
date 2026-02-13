// Simple counter in Flapjax
var countB = accumB(clicksE(dom('increment')), 0, function(count) { return count + 1; });
var display = DIV(TEXT(liftB(function(c) { return "Count: " + c; }, countB)));
dom('container').appendChild(display);
