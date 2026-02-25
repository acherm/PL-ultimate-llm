" Fibonacci sequence in Vim script
function! Fibonacci(n)
  if a:n <= 1
    return a:n
  endif
  let l:a = 0
  let l:b = 1
  let l:i = 2
  while l:i <= a:n
    let l:c = l:a + l:b
    let l:a = l:b
    let l:b = l:c
    let l:i += 1
  endwhile
  return l:b
endfunction

" Print first 10 Fibonacci numbers
let g:results = []
for i in range(10)
  call add(g:results, Fibonacci(i))
endfor
echo join(g:results, ', ')
