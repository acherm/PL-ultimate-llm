#lang rash

;; List files with their sizes
(for ([file (glob "*")])
  (printf "~a: ~a bytes\n"
          file
          (file-size file)))

;; Run a pipeline
|> ls -la |> grep ".rkt"
