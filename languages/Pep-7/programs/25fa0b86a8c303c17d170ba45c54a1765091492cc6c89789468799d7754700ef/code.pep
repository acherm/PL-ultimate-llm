BR main
n: .BLOCK 2
first: .BLOCK 2
second: .BLOCK 2
next: .BLOCK 2

main: DECI n,d
DECI first,d
DECI second,d
DECO first,d
CHARO '\n',i
DECO second,d
CHARO '\n',i
SUBSP 2,i

loop: LDA n,d
SUBA 2,i
STA n,d
BRLE done
LDA first,d
ADDA second,d
STA next,d
DECO next,d
CHARO '\n',i
LDA second,d
STA first,d
LDA next,d
STA second,d
BR loop

done: ADDSP 2,i
STOP
.END