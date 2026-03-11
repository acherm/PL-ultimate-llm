// Polyrhythmic pattern in Strudel live coding language
stack(
  note("c3 e3 g3 b3").sound("piano").slow(2),
  note("<a2 f2 bb2 c3>").sound("bass").slow(4),
  s("bd ~ sd hh").bank("RolandTR808")
).cpm(120 / 4)
