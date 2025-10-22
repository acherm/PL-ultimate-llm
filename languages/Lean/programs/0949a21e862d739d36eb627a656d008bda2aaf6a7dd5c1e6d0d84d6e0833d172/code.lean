theorem add_zero (n : Nat) : n + 0 = n := rfl

theorem zero_add (n : Nat) : 0 + n = n := by
  induction n with
  | zero => rfl
  | succ n ih => simp [add_succ, ih]

theorem add_succ (n m : Nat) : n + Nat.succ m = Nat.succ (n + m) := by
  induction n with
  | zero => simp [zero_add]
  | succ n ih => simp [add_succ, ih]

theorem succ_add (n m : Nat) : Nat.succ n + m = Nat.succ (n + m) := rfl

theorem add_comm (n m : Nat) : n + m = m + n := by
  induction n with
  | zero => simp [zero_add]
  | succ n ih => simp [add_succ, ih, succ_add]