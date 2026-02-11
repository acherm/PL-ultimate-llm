program ieee_example
  use, intrinsic :: iso_fortran_env
  use, intrinsic :: ieee_arithmetic
  implicit none

  real :: x, y
  logical :: flag

  x = 1.0
  y = 0.0

  ! Check for IEEE arithmetic support
  if (ieee_support_datatype(x)) then
    print *, "IEEE arithmetic is supported"
  end if

  ! Check for infinity
  x = x / y
  flag = ieee_is_finite(x)

  if (.not. flag) then
    print *, "Division by zero produced infinity"
  end if

  ! Test NaN
  x = 0.0 / y
  flag = ieee_is_nan(x)

  if (flag) then
    print *, "0/0 produced NaN as expected"
  end if

end program ieee_example