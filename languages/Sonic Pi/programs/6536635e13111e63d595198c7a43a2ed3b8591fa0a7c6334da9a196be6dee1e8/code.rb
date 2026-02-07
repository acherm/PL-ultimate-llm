# Simple melody with Sonic Pi
use_bpm 120

live_loop :melody do
  use_synth :piano
  play 60, release: 0.5
  sleep 0.5
  play 62, release: 0.5
  sleep 0.5
  play 64, release: 0.5
  sleep 0.5
  play 65, release: 0.5
  sleep 0.5
  play 67, release: 0.5
  sleep 0.5
  play 65, release: 0.5
  sleep 0.5
  play 64, release: 0.5
  sleep 0.5
  play 62, release: 0.5
  sleep 0.5
  play 60, release: 1.0
  sleep 1.0
end
