life←{⊃1 ⍵ ∨.∧ 3 4=+/,¯1 0 1∘.⊖¯1 0 1∘.⌽⊂⍵}
show←{⎕←(⊂'╭',(⍵-2)⍴'─','╮'),('│',[1](⍺{⍵/' ⍟'}¨⍺⍺),'│'),⊂'╰',(⍵-2)⍴'─','╯'}
⎕←'Enter size (e.g. 20): '
size←⎕
board←size size⍴0
board[1+⍳3;2]←1
board[2;3]←1
board[3;2]←1
{⍵ show size⊢board←life board}⍣≡1