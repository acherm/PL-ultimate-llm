.title  hello
        .psect  $code,pic,usr,con,rel,lcl,shr,exe,rd,nowrt,long
start:  .word   0
        pushaq  message
        calls   #1,g^lib$put_output
        ret
        .psect  $data,pic,usr,con,rel,lcl,noshr,noexe,rd,wrt,long
message: .ascid  /Hello, World!/
        .end    start
