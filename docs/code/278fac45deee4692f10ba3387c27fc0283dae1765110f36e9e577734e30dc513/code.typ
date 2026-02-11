#set document(title: "Fibonacci Sequence")
#set page(numbering: "1")
#set text(font: "Linux Libertine", size: 11pt)

= Fibonacci Sequence Generator

This document demonstrates a simple Typst function.

#let fib(n) = {
  if n <= 1 {
    n
  } else {
    fib(n - 1) + fib(n - 2)
  }
}

The first 10 Fibonacci numbers are:

#for i in range(10) {
  [- $F_(#i) = #fib(i)$]
}

#align(center)[
  _Generated with Typst_
]
