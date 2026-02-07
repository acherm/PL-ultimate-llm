program parallel_sum
  implicit none
  integer :: me, nproc, i
  real :: local_sum, total_sum[*]
  
  me = this_image()
  nproc = num_images()
  
  ! Each image computes its local sum
  local_sum = 0.0
  do i = me, 100, nproc
    local_sum = local_sum + real(i)
  end do
  
  ! Store result in coarray
  total_sum = local_sum
  
  sync all
  
  ! Image 1 collects all results
  if (me == 1) then
    local_sum = 0.0
    do i = 1, nproc
      local_sum = local_sum + total_sum[i]
    end do
    print *, "Total sum: ", local_sum
  end if
  
end program parallel_sum
