import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

n = 5  # number of qubits


def qft_rotations(circuit, n):
    """Apply Hadamard + controlled phase rotations (recursive QFT core)."""
    if n == 0:
        return circuit
    n -= 1
    circuit.h(n)
    for qubit in range(n):
        circuit.cp(np.pi / 2 ** (n - qubit), qubit, n)
    qft_rotations(circuit, n)


def swap_registers(circuit, n):
    """Step 4: Swap qubits to correct the QFT ordering."""
    for qubit in range(n // 2):
        circuit.swap(qubit, n - qubit - 1)
    return circuit


def qft(circuit, n):
    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit


# Step: Create a quantum circuit with 5 qubits
qc = QuantumCircuit(n, n)

# Initial state: start in |00000> then encode an example basis state, e.g. |00011> (= 3)
qc.x(0)
qc.x(1)
qc.barrier()

# Apply the 5-qubit QFT
qft(qc, n)
qc.barrier()

qc.measure(range(n), range(n))
print(qc.draw(output='text', fold=120))

simulator = AerSimulator()
job = simulator.run(qc, shots=2048)
result = job.result()
counts = result.get_counts()

print("\nMeasurement counts:")
print(counts)

plot_histogram(counts, title="5-Qubit Quantum Fourier Transform Output")
plt.tight_layout()
plt.savefig("assignment5_output.png", dpi=120)
print("\nHistogram saved as assignment5_output.png")