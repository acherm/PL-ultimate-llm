theory Example
imports Main
begin

theorem example: "A ∧ B ⟶ B ∧ A"
proof
  assume "A ∧ B"
  then have "A" ..
  moreover from ‹A ∧ B› have "B" ..
  ultimately show "B ∧ A" ..
qed

theorem addition_commutative: "(x::nat) + y = y + x"
  by auto

lemma conjunction_example:
  assumes "P" and "Q"
  shows "P ∧ Q"
proof -
  from assms show ?thesis by auto
qed

end
