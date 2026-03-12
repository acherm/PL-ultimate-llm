abstract Foods = {
  cat Comment ; Kind ; Quality ;
  fun Pred : Kind -> Quality -> Comment ;
  fun Wine, Pizza, Cheese : Kind ;
  fun Good, Bad, Delicious : Quality ;
}

concrete FoodsEng of Foods = {
  lincat Comment, Kind, Quality = {s : Str} ;
  lin Pred k q = {s = k.s ++ " is " ++ q.s} ;
  lin Wine = {s = "wine"} ;
  lin Pizza = {s = "pizza"} ;
  lin Cheese = {s = "cheese"} ;
  lin Good = {s = "good"} ;
  lin Bad = {s = "bad"} ;
  lin Delicious = {s = "delicious"} ;
}
