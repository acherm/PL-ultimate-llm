/*
 * canon.ck
 * 
 * Pachelbel's Canon in D
 * 
 * by Perry R. Cook, 2005
 * 
 * This is a four-part canon, with the parts entering
 * at two measure intervals.  The bass line is two measures
 * long and repeats throughout.  The three violin parts
 * are identical, but delayed in time.
 * 
 */

// Two measures of bass line
[ 62, 58, 60, 55, 57, 53, 57, 58 ] @=> int bassLine[];

// One measure of violin melody
[ 69, 73, 74, 73, 71, 69, 71, 68 ] @=> int violin1[];
[ 69, 66, 68, 64, 66, 62, 66, 68 ] @=> int violin2[];

fun void playViolin( Sitar s, float gain )
{
    s.gain(gain);
    for (0 => int i; i < 8; i++ ) {
        for (0 => int j; j < 8; j++) {
            Std.mtof(violin1[j]) => s.freq;
            120::ms => now;
        }
        for (0 => int j; j < 8; j++) {
            Std.mtof(violin2[j]) => s.freq;
            120::ms => now;
        }
    }
}

fun void playBass( Rhodey r, float gain )
{
    r.gain(gain);
    while(1) {
        for (0 => int i; i < 8; i++) {
            Std.mtof(bassLine[i]) => r.freq;
            480::ms => now;
        }
    }
}

Rhodey bass => dac;
Sitar violinSection[3];

for (0 => int i; i < 3; i++) {
    violinSection[i] => dac;
}

spork ~ playBass(bass, 0.4);

for (0 => int i; i < 3; i++) {
    spork ~ playViolin(violinSection[i], 0.4 - i*0.08);
    16 * 120::ms => now;
}