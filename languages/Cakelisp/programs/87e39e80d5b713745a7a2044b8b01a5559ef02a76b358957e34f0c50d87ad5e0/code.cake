(defun-local audio-dump-recorded-buffer (output-filename (* (const char))
                                         buffer (* Uint8)
                                         buffer-size int)
  (var dest-file (* FILE) (fopen output-filename "w"))
  (unless dest-file
    (printf "Could not open file to write data\n")
    (return))

  (var i int 0)
  (while (< i buffer-size)
    (fprintf dest-file "%d %d\n" i (at i buffer))
    (incr i))
  (fclose dest-file))
