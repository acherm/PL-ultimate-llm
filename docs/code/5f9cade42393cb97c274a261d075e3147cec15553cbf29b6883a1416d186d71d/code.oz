declare
  fun {QuickSort Xs}
     case Xs
     of nil then nil
     [] Pivot|Xr then
        Left Right
     in
        {Partition Xr Pivot Left Right}
        {Append {QuickSort Left} Pivot|{QuickSort Right}}
     end
  end

  proc {Partition Xs Pivot ?Left ?Right}
     Left = {Filter Xs fun {$ X} X < Pivot end}
     Right = {Filter Xs fun {$ X} X >= Pivot end}
  end
in
  {Show {QuickSort [3 1 4 1 5 9 2 6 5 3 5]}}
  {Show {QuickSort [8 7 6 5 4 3 2 1]}}
  {Show {QuickSort [1]}}
  {Show {QuickSort nil}}