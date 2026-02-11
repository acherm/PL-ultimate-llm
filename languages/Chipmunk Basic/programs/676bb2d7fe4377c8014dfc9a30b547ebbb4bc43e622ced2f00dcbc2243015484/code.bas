10 rem Number Guessing Game
20 randomize timer
30 target = int(rnd(1) * 100) + 1
40 attempts = 0
50 print "I'm thinking of a number between 1 and 100."
60 print
70 input "Enter your guess: "; guess
80 attempts = attempts + 1
90 if guess < target then print "Too low! Try again." : goto 70
100 if guess > target then print "Too high! Try again." : goto 70
110 print "Congratulations! You guessed it in "; attempts; " attempts."
120 end
