// Gibber - Audiovisual performance coding
// Simple drum pattern with FM synthesis

drums = EDM('x*ox*xo-').play()

fm = FM('bass')
  .note.seq([0,3,7,10], 1/4)
  .play()

drums.fx.add(Delay(1/3))
fm.fx.add(Reverb())
