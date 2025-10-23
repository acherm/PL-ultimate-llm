\version "2.24.0"

melody = \relative c'' {
  \time 3/4
  \partial 4
  e4 | \numericTimeSignature
  d4. e8 f4 | g4. f8 e4 | d4 b'4. a8 | g4. f8 e4 |
  d4. e8 f4 | e4. d8 cis4 | d2 r4 \bar "|" \break
  e4 | \numericTimeSignature
  d4. e8 f4 | g4. f8 e4 | f4. e8 d4 | cis2. \bar "||"
}

\score {
  \new Staff \with {
    instrumentName = "Clarinet"
  }
  \melody
  \layout { }
  \midi { }
}