begin
  procedure quicksort(A, low, high);
    value low, high;
    integer low, high;
    real array A;
  begin
    integer i, j;
    real pivot, temp;

    if low < high then
    begin
      pivot := A[low];
      i := low;
      j := high;

      for j := j step -1 until i do
      begin
        while A[i] < pivot do i := i + 1;
        while A[j] > pivot do j := j - 1;

        if i < j then
        begin
          temp := A[i];
          A[i] := A[j];
          A[j] := temp;
        end;
      end;

      temp := A[low];
      A[low] := A[j];
      A[j] := temp;

      quicksort(A, low, j - 1);
      quicksort(A, j + 1, high);
    end;
  end quicksort;
end
