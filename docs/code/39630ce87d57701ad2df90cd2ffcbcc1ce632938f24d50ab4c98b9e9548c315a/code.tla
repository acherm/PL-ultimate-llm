(*--algorithm TwoPhase

variables rm_state = [r \in RM |-> "working"],
          tm_state = "init",
          tm_decision,
          msgs = {};

define
  PreparedRMs == {r \in RM : rm_state[r] = "prepared"}
  RMReplies(M)  == {m \in msgs : m.type = M}
end define;

process TM = "TM"
variables vote_reqs = RM;
begin
  T1: \* Send vote requests to all RMs
      while vote_reqs /= {} do
        with r \in vote_reqs do
          msgs := msgs \union {[type |-> "VoteRequest", dest |-> r]};
          vote_reqs := vote_reqs \ {r};
        end with;
      end while;
      tm_state := "waiting";

  T2: \* Wait for votes from all RMs
      await \A r \in RM : \E m \in RMReplies("Vote"): m.rm = r;

  T3: either \* Commit
        await \A m \in RMReplies("Vote"): m.vote = "commit";
        tm_decision := "commit";
        tm_state := "committed";
      or \* Abort
        await \E m \in RMReplies("Vote"): m.vote = "abort";
        tm_decision := "abort";
        tm_state := "aborted";
      end either;

  T4: either \* Send commit messages
        await tm_decision = "commit";
        with r \in RM do
          msgs := msgs \union {[type |-> "Commit", dest |-> r]};
        end with;
      or \* Send abort messages
        await tm_decision = "abort";
        with r \in RM do
          msgs := msgs \union {[type |-> "Abort", dest |-> r]};
        end with;
      end either;
end process;

process RMProc \in RM
variable vote;
begin
  R1: \* Receive vote request
      await \E m \in msgs: (m.type = "VoteRequest") /\ (m.dest = self);
      rm_state[self] := "prepared";

  R2: either \* Vote to commit
        vote := "commit";
      or \* Vote to abort
        vote := "abort";
      end either;
      msgs := msgs \union {[type |-> "Vote", rm |-> self, vote |-> vote]};

  R3: either \* Receive commit
        await \E m \in msgs: (m.type = "Commit") /\ (m.dest = self);
        rm_state[self] := "committed";
      or \* Receive abort
        await \E m \in msgs: (m.type = "Abort") /\ (m.dest = self);
        rm_state[self] := "aborted";
      end either;
end process;

end algorithm; *)