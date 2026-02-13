program fibonacci
  implicit none
  integer :: n, i
  integer :: fib_prev, fib_curr, fib_next

  print *, 'Enter number of Fibonacci terms:'
  read *, n

  if (n < 1) then
    print *, 'Please enter a positive integer'
    stop
  end if

  fib_prev = 0
  fib_curr = 1

  print *, 'Fibonacci sequence:'
  print *, fib_prev

  if (n > 1) then
    print *, fib_curr
  end if

  do i = 3, n
    fib_next = fib_prev + fib_curr
    print *, fib_next
    fib_prev = fib_curr
    fib_curr = fib_next
  end do

end program fibonacci
