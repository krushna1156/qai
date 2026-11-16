from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Step 1 & 2: Initialize registers and create the circuit
n_qubits = 16
qc = QuantumCircuit(n_qubits, n_qubits)

# Step 3: Apply a Hadamard gate to all qubits (creates superposition)
qc.h(range(n_qubits))

# Step 4: Measure the qubits
qc.measure(range(n_qubits), range(n_qubits))

print(qc.draw(output='text'))

# Execute on Aer simulator
simulator = AerSimulator()
job = simulator.run(qc, shots=1)
result = job.result()
counts = result.get_counts()

random_bitstring = list(counts.keys())[0]
random_number = int(random_bitstring, 2)

print(f"\nRandom 16-bit string: {random_bitstring}")
print(f"Random number (decimal): {random_number}")

# Run multiple shots to show distribution
job_multi = simulator.run(qc, shots=1024)
counts_multi = job_multi.result().get_counts()

plot_histogram(counts_multi, title="16-Qubit RNG Output Distribution (top outcomes)")
plt.tight_layout()
plt.savefig("assignment1_output.png", dpi=120)
print("\nHistogram saved as assignment1_output.png")