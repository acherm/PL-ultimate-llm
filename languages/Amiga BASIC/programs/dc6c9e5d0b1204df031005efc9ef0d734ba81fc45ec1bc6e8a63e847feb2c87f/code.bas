REM Number Guessing Game
REM A simple game where the computer picks a number and you guess it
CLS
PRINT "Number Guessing Game"
PRINT "===================="
PRINT
number = INT(RND * 100) + 1
guesses = 0
PRINT "I'm thinking of a number between 1 and 100."
PRINT
DO
    INPUT "Enter your guess: ", guess
    guesses = guesses + 1
    IF guess < number THEN
        PRINT "Too low! Try again."
    ELSEIF guess > number THEN
        PRINT "Too high! Try again."
    ELSE
        PRINT "Correct! You guessed it in"; guesses; "tries."
        EXIT DO
    END IF
LOOP
