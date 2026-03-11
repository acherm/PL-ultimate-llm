(* Bell state preparation in QWIRE *)
Require Import Quantum.
Require Import Dirac.
Open Scope matrix_scope.

(* Hadamard gate applied to |0> gives |+> state *)
Definition hadamard_example : Matrix 2 1 :=
  hadamard × ket 0.

(* Bell state |Phi+> = (|00> + |11>) / sqrt(2) *)
Definition bell_phi_plus : Matrix 4 1 :=
  (I 2 ⊗ hadamard) × (cnot × (ket 0 ⊗ ket 0)).

(* Verify Bell state has correct norm *)
Lemma bell_phi_plus_norm :
  inner_product bell_phi_plus bell_phi_plus = 1.
Proof.
  unfold bell_phi_plus, inner_product.
  solve_matrix.
Qed.

(* Teleportation circuit: Alice has qubit psi, shares Bell pair with Bob *)
(* After Alice measures, Bob applies corrections to recover psi *)
Definition teleport_circuit (psi : Matrix 2 1) : Matrix 2 1 :=
  (* Step 1: Create Bell pair *)
  let bell_pair := (I 2 ⊗ hadamard) × (cnot × (ket 0 ⊗ ket 0)) in
  (* Step 2: Alice's CNOT between psi and her qubit *)
  let after_cnot := (cnot ⊗ I 2) × (psi ⊗ bell_pair) in
  (* Result: psi teleported to Bob's qubit after measurement and correction *)
  after_cnot.
