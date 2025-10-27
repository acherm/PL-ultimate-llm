(
SynthDef("help_SinOsc", { | freq=440, gate=0 |
    var z;
    z = SinOsc.ar(freq, 0, 0.1) * EnvGen.kr(Env.asr(0.01, 1, 1), gate, doneAction:2);
    Out.ar(0, z ! 2)
}).send(s);
)

~synth = Synth("help_SinOsc");
~synth.set("gate", 1);