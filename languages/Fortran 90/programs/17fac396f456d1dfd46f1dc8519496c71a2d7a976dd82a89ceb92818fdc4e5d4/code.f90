program matrix_multiply
  implicit none
  integer, parameter :: n = 3
  real, dimension(n,n) :: a, b, c
  integer :: i, j, k

  ! Initialize matrices
  a = reshape([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0], [n, n])
  b = reshape([9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0], [n, n])

  ! Matrix multiplication
  do i = 1, n
    do j = 1, n
      c(i,j) = 0.0
      do k = 1, n
        c(i,j) = c(i,j) + a(i,k) * b(k,j)
      end do
    end do
  end do

  ! Print result
  print *, 'Result matrix C:'
  do i = 1, n
    print '(3F8.2)', (c(i,j), j=1,n)
  end do

end program matrix_multiply
