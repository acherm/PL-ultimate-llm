# Fibonacci sequence in Parrot Assembly Language (PASM)
# Prints the first 15 Fibonacci numbers

    set I0, 0       # a (current term)
    set I1, 1       # b (next term)
    set I2, 15      # counter

LOOP:
    unless I2, END
    print I0
    print "\n"
    set I3, I0
    add I3, I1
    set I0, I1
    set I1, I3
    dec I2
    branch LOOP

END:
    end
