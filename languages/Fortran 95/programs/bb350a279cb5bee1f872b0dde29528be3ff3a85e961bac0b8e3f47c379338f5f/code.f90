program bubble_sort
    implicit none
    integer, parameter :: n = 10
    integer :: array(n)
    integer :: i, j, temp
    logical :: swapped

    ! Initialize array
    array = (/64, 34, 25, 12, 22, 11, 90, 88, 45, 50/)

    print *, 'Original array:'
    print *, array

    ! Bubble sort algorithm
    do i = 1, n-1
        swapped = .false.
        do j = 1, n-i
            if (array(j) > array(j+1)) then
                temp = array(j)
                array(j) = array(j+1)
                array(j+1) = temp
                swapped = .true.
            end if
        end do
        if (.not. swapped) exit
    end do

    print *, 'Sorted array:'
    print *, array

end program bubble_sort