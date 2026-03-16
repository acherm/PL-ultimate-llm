(define LED 13)

(arduino-set-pin-mode! LED output)

(let loop ()
  (arduino-digital-write! LED high)
  (arduino-delay 500)
  (arduino-digital-write! LED low)
  (arduino-delay 500)
  (loop))
