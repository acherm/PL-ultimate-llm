let permute_element vec n p =
  let aux = vec.(n) in
  vec.(n) <- vec.(p);
  vec.(p) <- aux;;

let choose_pivot vec start finish = start;;

let permute_pivot vec start finish ind_pivot =
  permute_element vec start ind_pivot;
  let i = ref (start+1) and j = ref finish and pivot = vec.(start) in
  while !i < !j do
    if vec.(!j) >= pivot then decr j
    else
    begin
      permute_element vec !i !j;
      incr i
    end
  done;
  if vec.(!i) > pivot then decr i;
  permute_element vec start !i;
  !i;;

let rec quick vec start finish =
  if start < finish
  then
    let pivot = choose_pivot vec start finish in
    let place_pivot = permute_pivot vec start finish pivot in
    quick (quick vec start (place_pivot-1)) (place_pivot+1) finish
  else vec;;

let quicksort vec = quick vec 0 ((Array.length vec)-1);;
