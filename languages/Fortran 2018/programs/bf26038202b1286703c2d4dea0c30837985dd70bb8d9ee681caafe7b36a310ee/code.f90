program fortran2018_demo
  implicit none
  integer :: i, n
  real :: sum_val
  
  ! Fortran 2018 feature: error stop with message
  n = -5
  if (n < 0) then
    error stop "Error: n must be non-negative"
  end if
  
  sum_val = 0.0
  do i = 1, n
    sum_val = sum_val + real(i)
  end do
  
  print *, "Sum from 1 to", n, "is", sum_val
  
end program fortran2018_demo
