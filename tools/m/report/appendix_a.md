---

## Appendix A — The review tool

`tools/m/review_app.py` is a dependency-free `http.server` app (port 8769) over
every label layer of the study. It follows the cobol/fsf/rpgle apps — append-only
JSON reviews under `reviews_m/<sha1_git>/`, group rules in
`reviews_m/_rules.jsonl`, git as the sync layer — and adds what the revised
method needs.

```bash
python3 -m tools.m.review_app --reviewer <your-id>     # http://127.0.0.1:8769
```

**Dashboard.** Language by frame (by-file, by-repo, and the 25 largest
repositories), each labeller's agreement and abstention against the primary judge
— labelled explicitly as *not* ground truth — provenance kinds, and one-click
work queues for every disagreement type: judges disagree, judge ≠ our rules,
Pygments ≠ judge, Synid `Text`/unresolved, Linguist abstains, the Octave
lexical/semantic split, the non-Objective-C/MATLAB tail, non-hand-written files.

![Review app — dashboard](assets/m/app_dashboard.png)

**Browse.** Filter by frame, judge language, flag, or name/origin; each row shows
all seven labellers as coloured tags (agrees with the judge / disagrees /
abstains), so a column of red is a tool's failure mode at a glance.

![Review app — browse](assets/m/app_list.png)

**Detail.** Source with line numbers; a provenance panel with the forge link *at
the archived branch*, the SWH browse context and the qualified SWHID, plus three
population signals the judge never saw — contents in the repository, archived
versions of this path, and how many repositories carry this file name; all seven
labellers with their raw answers; both judges' full verdicts side by side with
differences shaded; the non-zero mechanical indicators; a review form; and a
group-rule form (scope: origin, filename regex, or path regex).

![Review app — detail](assets/m/app_detail.png)

**Blind audit.** `/audit` lists the stratified queue (§5.8) with a progress bar and
the live weighted accuracy of every labeller. Items open in blind mode: the
machine panels are hidden until the reviewer saves, then revealed for comparison.
`Save & next` (or the `n` key) walks the queue. Reviews record whether they were
made blind.

![Review app — blind audit item](assets/m/app_blind.png)
