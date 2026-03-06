program main
  implicit none
  write(*,'(a,i0,a,i0,a)') 'Hello from image ', this_image(), ' of ', num_images(), '!'
  sync all
end program main
