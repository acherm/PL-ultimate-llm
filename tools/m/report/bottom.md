`.m` is two languages sharing one extension, plus a thin
> tail of seven more. **Which of the two is "the" `.m` language depends on what you
> count:** by file, Objective-C 54% and MATLAB 43%; by repository, 71% and 27%;
> by `(repository, path)` with version history collapsed, a near tie (50% / 47%). **Much of it was not written by the
> project that holds it:** 22% of Objective-C files — and 58% of Objective-C files
> drawn one per repository — are Xcode templates, CocoaPods stubs, vendored libraries or
> decompiled firmware — and content deduplication cannot merge them, because Xcode
> personalises the header of every copy. **The identifiers the ecosystem relies on each
> fail on one specific, fixable pattern:** Pygments reads MATLAB matrix literals as
> Objective-C (12% of MATLAB files); Linguist's rules abstain on MATLAB without a
> `%` comment (14%); Software Heritage's own Synid answers "Text" for one
> Objective-C file in ten — its comment heuristic counts the `%` in `@"%@"` — and,
> run on local files, never content-identified a file that is not UTF-8. Our own mapping gives `.m` to
> three unrelated languages through an extension-based join that affects 19% of
> its Pygments links.
>
> **Methodologically**, no labeller was treated as the oracle: seven labellers
> (three of them the ecosystem's own tools), a judge kept blind to our features, a
> second judge from another vendor, predictions committed before judging, and a
> weighted blind human audit ready to run. The two judges agree on the language
> of 99.2% of files (κ 0.98), but not on whether MATLAB code is portable to Octave
> — where they give opposite majority answers.
