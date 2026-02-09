pragma circom 2.0.0;

template Multiplier2() {
    signal input a;
    signal input b;
    signal output c;

    c <== a * b;
}

template MultiplierN(n) {
    signal input in[n];
    signal output out;

    component muls[n - 1];
    for (var i = 0; i < n - 1; i++) {
        muls[i] = Multiplier2();
    }

    muls[0].a <== in[0];
    muls[0].b <== in[1];
    for (var i = 1; i < n - 1; i++) {
        muls[i].a <== muls[i - 1].c;
        muls[i].b <== in[i + 1];
    }

    out <== muls[n - 2].c;
}

component main = MultiplierN(4);
