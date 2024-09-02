
from typing import List
from .qubit import QubitCollection
from .bitgate import *

def bitwiseX(qc: QubitCollection) -> None:
    for q in qc.qubits:
        X(q)

def maskedBitwiseX(qc: QubitCollection, mask: int) -> None:
    for q in qc.qubits:
        if mask & 1:
            X(q)
        mask >>= 1

def bitwiseCNOT(control: QubitCollection, target: QubitCollection) -> None:
    if len(control.qubits) != len(target.qubits):
        raise ValueError("Control and target qubit collections must have the same length")
    
    for c, t in zip(control.qubits, target.qubits):
        CNOT(c, t)

def measure(qc: QubitCollection) -> int:
    if len(qc.qubits) == 0:
        raise ValueError("Cannot measure an empty qubit collection")
    
    results = sum([bit_measure(q) * (1 << i) for i, q in enumerate(qc.qubits)])

    return results

def bitwiseH(qc: QubitCollection) -> None:
    for q in qc.qubits:
        H(q)

def bitwiseMCX(controls: List[QubitCollection], target: QubitCollection) -> None:
    if len(controls) == 0:
        raise ValueError("Cannot perform a multi-controlled X gate with no control qubits")
    
    for c in controls:
        if len(c.qubits) != len(target.qubits):
            raise ValueError("Control and target qubit collections must have the same length")
    
    for i in range(len(target.qubits)):
        MCX([c.qubits[i] for c in controls], target.qubits[i])

def bitwiseZ(qc: QubitCollection) -> None:
    for q in qc.qubits:
        Z(q)

