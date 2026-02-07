100 REMark Sieve of Eratosthenes in SuperBASIC
110 DEFine PROCedure sieve(limit)
120   LOCal flags%(limit), i, j, count
130   FOR i = 2 TO limit
140     flags%(i) = 1
150   END FOR i
160   count = 0
170   FOR i = 2 TO limit
180     IF flags%(i) = 1 THEN
190       count = count + 1
200       PRINT i;" ";
210       j = i * i
220       REPeat mark_loop
230         IF j > limit THEN EXIT mark_loop
240         flags%(j) = 0
250         j = j + i
260       END REPeat mark_loop
270     END IF
280   END FOR i
290   PRINT
300   PRINT "Found "; count; " primes up to "; limit
310 END DEFine sieve
320 :
330 PRINT "Primes up to 100:"
340 sieve 100
