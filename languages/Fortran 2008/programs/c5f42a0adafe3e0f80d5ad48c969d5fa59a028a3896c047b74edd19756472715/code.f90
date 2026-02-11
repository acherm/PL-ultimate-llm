program concurrent_example
  implicit none
  integer, parameter :: n = 1000
  real :: a(n), b(n), c(n)
  integer :: i

  ! Initialize arrays
  do i = 1, n
    a(i) = real(i)
    b(i) = real(i) * 2.0
  end do

  ! Fortran 2008 DO CONCURRENT - allows parallel execution
  do concurrent (i = 1:n)
    c(i) = a(i) + b(i)
  end do

  ! Print first and last elements
  print *, "First element: c(1) = ", c(1)
  print *, "Last element: c(n) = ", c(n)
  print *, "Sum of all elements: ", sum(c)

end program concurrent_example