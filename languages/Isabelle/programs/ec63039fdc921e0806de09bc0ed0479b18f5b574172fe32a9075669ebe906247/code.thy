datatype bool = true | false

fun not :: "bool ⇒ bool" where
"not true = false" |
"not false = true"

lemma "not (not true) = true"
  by auto