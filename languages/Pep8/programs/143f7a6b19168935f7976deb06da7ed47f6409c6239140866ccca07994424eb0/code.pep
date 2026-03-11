;Program to output Fibonacci numbers in Pep/8 assembly
BR      main
;
n1:     .WORD   1
n2:     .WORD   1
temp:   .WORD   0
count:  .WORD   0
;
main:   DECO    n1,d
        CHARO   '\n',i
        DECO    n2,d
        CHARO   '\n',i
        LDA     2,i
        STA     count,d
loop:   LDA     count,d
        SUBA    8,i
        BRGE    done
        LDA     n1,d
        ADDA    n2,d
        STA     temp,d
        LDA     n2,d
        STA     n1,d
        LDA     temp,d
        STA     n2,d
        DECO    n2,d
        CHARO   '\n',i
        LDA     count,d
        ADDA    1,i
        STA     count,d
        BR      loop
done:   STOP
        .END