/ Simple addition program for PDP-9
/ Adds two numbers and stores result

        *200            / Start at location 200
        LAC NUM1        / Load AC with first number
        ADD NUM2        / Add second number
        DAC RESULT      / Deposit AC in result
        HLT             / Halt

NUM1,   5               / First number
NUM2,   7               / Second number
RESULT, 0               / Result location
