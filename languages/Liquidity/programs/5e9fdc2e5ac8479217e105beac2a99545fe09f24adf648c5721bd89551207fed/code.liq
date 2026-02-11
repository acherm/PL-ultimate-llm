[%%version 2.0]

type storage = {
  balances : (address, nat) big_map;
  total_supply : nat;
}

let%init storage total_supply =
  let owner = Current.sender () in
  {
    balances = BigMap.add owner total_supply (BigMap []);
    total_supply = total_supply;
  }

let%entry transfer (dest : address) (amount : nat) storage =
  let sender = Current.sender () in
  let sender_balance = match BigMap.find sender storage.balances with
    | None -> 0p
    | Some balance -> balance
  in
  if sender_balance < amount then
    failwith "Insufficient balance"
  else
    let new_sender_balance = sender_balance - amount in
    let dest_balance = match BigMap.find dest storage.balances with
      | None -> 0p
      | Some balance -> balance
    in
    let new_dest_balance = dest_balance + amount in
    let balances = BigMap.add sender new_sender_balance storage.balances in
    let balances = BigMap.add dest new_dest_balance balances in
    ( [], { storage with balances = balances } )
