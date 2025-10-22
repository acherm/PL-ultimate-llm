if exists("g:loaded_whitespace") || &cp
  finish
endif
let g:loaded_whitespace = 1

command! -nargs=0 WhitespaceToggle call whitespace#toggle()

function! whitespace#toggle()
  if exists("b:whitespace_on") && b:whitespace_on
    let b:whitespace_on = 0
    setlocal nolist
    echo "Whitespace off"
  else
    let b:whitespace_on = 1
    setlocal list
    setlocal listchars=tab:»·,trail:·,eol:¬,nbsp:·
    echo "Whitespace on"
  endif
endfunction