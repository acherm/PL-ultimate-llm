NEURON {
    SUFFIX pas
    NONSPECIFIC_CURRENT i
    RANGE g, e
}

PARAMETER {
    g = .001 (siemens/cm2)
    e = -70 (millivolt)
}

ASSIGNED {
    v (millivolt)
    i (milliamp/cm2)
}

BREAKPOINT {
    i = g*(v - e)
}
