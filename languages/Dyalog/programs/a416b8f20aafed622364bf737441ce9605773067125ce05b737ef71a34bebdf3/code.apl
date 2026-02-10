⍝ Conway's Game of Life
⍝ Simple implementation in Dyalog APL
life←{
    ⍝ Count living neighbors using stencil
    n←{+⌿,¯1 0 1∘.⊖¯1 0 1∘.⌽⊂⍵}
    ⍝ Apply rules: born if 3 neighbors, survive if 2 or 3
    {(3=⍵)∨⍵∧2=⍵}n ⍵
}

⍝ Example: glider pattern
glider←3 3⍴0 1 0 0 0 1 1 1 1