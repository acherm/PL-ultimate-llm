/ PDP-5 ASSEMBLY PROGRAM - ADD TWO NUMBERS
/
        *200            / ORIGIN AT 200 OCTAL
START,  CLA             / CLEAR ACCUMULATOR
        TAD NUM1        / ADD FIRST NUMBER
        TAD NUM2        / ADD SECOND NUMBER
        DCA RESULT      / STORE RESULT
        HLT             / HALT
/
NUM1,   7777            / FIRST NUMBER
NUM2,   0001            / SECOND NUMBER
RESULT, 0000            / RESULT STORAGE
/
        $START          / END WITH START ADDRESS
