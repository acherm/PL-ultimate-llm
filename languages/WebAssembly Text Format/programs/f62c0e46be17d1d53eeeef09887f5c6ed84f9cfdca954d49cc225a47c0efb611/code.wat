(module
  ;; Import the required fd_write function from the WASI environment
  (import "wasi_snapshot_preview1" "fd_write" (func $fd_write (param i32 i32 i32 i32) (result i32)))

  (memory (export "memory") 1)

  ;; Store the string "hello world\n" in memory
  ;; The string is 12 bytes long
  (data (i32.const 0) "hello world\n")

  (func (export "_start")
    ;; Define the arguments for fd_write
    ;; `iovs` is a pointer to a pair of `iovec` structs
    ;; We need to write the `iovec` structs into memory
    ;; iovec struct: { buf: i32, buf_len: i32 }
    ;; We'll place the iovec at address 12 (after the string)

    ;; First iovec
    (i32.store (i32.const 12) (i32.const 0))  ;; buf: pointer to the string at address 0
    (i32.store (i32.const 16) (i32.const 12)) ;; buf_len: length of the string

    ;; Call fd_write
    (call $fd_write
      (i32.const 1)   ;; fd: 1 for stdout
      (i32.const 12)  ;; iovs: pointer to the iovecs
      (i32.const 1)   ;; iovs_len: number of iovecs
      (i32.const 20)  ;; nwritten: pointer to a location to store the number of bytes written
    )
    drop ;; Discard the result of fd_write
  )
)