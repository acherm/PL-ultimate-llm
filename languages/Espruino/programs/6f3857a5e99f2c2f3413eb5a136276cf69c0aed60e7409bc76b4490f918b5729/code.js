// Blink an LED on pin B1
var on = false;
setInterval(function() {
  on = !on;
  LED1.write(on);
}, 500);