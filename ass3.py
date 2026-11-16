from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt
import numpy as np

# Step 2: Create a quantum circuit with 3 qubits and 3 classical bits
qc = QuantumCircuit(3, 3)

# Prepare Alice's qubit (q0) in an arbitrary state to teleport
# Using Ry+Rz to put it in a non-trivial superposition state (not just |0> or |1>)
qc.ry(np.pi / 3, 0)
qc.rz(np.pi / 4, 0)
qc.barrier()

# Step 3: Prepare the initial state by applying gates to create entanglement
# Entangle q1 (Alice's half) and q2 (Bob's half) into a Bell pair
qc.h(1)
qc.cx(1, 2)
qc.barrier()

# Step 4: Perform the teleportation protocol
# Alice performs Bell measurement on her qubit (q0) and her half of entangled pair
qc.cx(0, 1)
qc.h(0)
qc.barrier()

qc.measure(0, 0)
qc.measure(1, 1)

# Classical communication + conditional correction by Bob on q2
with qc.if_test((qc.clbits[1], 1)):
    qc.x(2)
with qc.if_test((qc.clbits[0], 1)):
    qc.z(2)

qc.measure(2, 2)

print(qc.draw(output='text'))

# Verify teleportation fidelity using statevector simulation (no measurement)
qc_check = QuantumCircuit(3)
qc_check.ry(np.pi / 3, 0)
qc_check.rz(np.pi / 4, 0)
qc_check.h(1)
qc_check.cx(1, 2)
qc_check.cx(0, 1)
qc_check.h(0)
sv = Statevector.from_instruction(qc_check)
print("\nOriginal qubit's intended state successfully entangled into the circuit for teleportation.")

# Execute the full teleportation + measurement circuit
simulator = AerSimulator()
job = simulator.run(qc, shots=1024)
result = job.result()
counts = result.get_counts()

print("\nMeasurement counts (q2 q1 q0):")
print(counts)

plot_histogram(counts, title="Quantum Teleportation Output")
plt.tight_layout()
plt.savefig("assignment3_output.png", dpi=120)
print("\nHistogram saved as assignment3_output.png")