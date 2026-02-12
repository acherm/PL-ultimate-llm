#lang scribble/base

@title{Getting Started with Scribble}

@section{Introduction}

Scribble is a documentation language that allows you to write
documentation with embedded code examples.

@codeblock|{
#lang racket
(define (factorial n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))
}|

This function computes the @italic{factorial} of a number.
