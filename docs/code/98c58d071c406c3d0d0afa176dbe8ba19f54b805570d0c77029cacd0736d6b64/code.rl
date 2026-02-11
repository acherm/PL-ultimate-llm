machine csv;

action a1 {
  puts "field: ";
}

action a2 {
  puts "record\n";
}

  csv :=
    (   (   field % a1
        ) (   ',' field
            )*
      ) % a2
    ;

field :=
  ^(',' | '\n')+ ;

main := csv* ;