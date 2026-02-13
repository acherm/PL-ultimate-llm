program hello_fortran2023
    implicit none
    character(len=50) :: name
    integer :: year

    ! Fortran 2023 example
    print *, "Enter your name:"
    read *, name

    year = 2023
    print *, "Hello, ", trim(name), "!"
    print *, "Welcome to Fortran", year

end program hello_fortran2023