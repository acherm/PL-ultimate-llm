from QGL import *

def Ramsey(qubit, delays):
    """Ramsey fringe experiment for T2* measurement."""
    seqs = []
    for d in delays:
        seqs.append([X90(qubit), Id(qubit, length=d), X90(qubit), MEAS(qubit)])
        seqs.append([X90(qubit), Id(qubit, length=d), X90m(qubit), MEAS(qubit)])
    return seqs

def T1(qubit, delays):
    """T1 decay experiment for qubit lifetime measurement."""
    seqs = []
    for d in delays:
        seqs.append([X(qubit), Id(qubit, length=d), MEAS(qubit)])
        seqs.append([Id(qubit, length=d), MEAS(qubit)])
    return seqs
