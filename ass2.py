from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, pauli_error
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Step 1: Identify the noisy channel
# We simulate a bit-flip noise channel (probability p that X error occurs)
p_error = 0.3
bit_flip = pauli_error([('X', p_error), ('I', 1 - p_error)])

noise_model = NoiseModel()
noise_model.add_all_qubit_quantum_error(bit_flip, ['id', 'x'])

# Step 2 & 3: Choose error correction technique + implement detection/correction
# 3-qubit bit-flip repetition code
qc = QuantumCircuit(5, 3)  # 3 data/code qubits + 2 ancilla for syndrome, 3 classical bits for readout

# Prepare logical qubit in state |1> (arbitrary choice) and encode
qc.x(0)  # set logical qubit to |1>
qc.cx(0, 1)
qc.cx(0, 2)  # qubits 0,1,2 now hold the encoded logical state |111>
qc.barrier()

# Simulate noise: force an artificial bit-flip error on qubit 1
qc.id(1)  # 'id' gate is where noise_model injects the bit-flip error
qc.barrier()

# ---- Step 3: Error detection using syndrome ancillas
qc.cx(0, 3)
qc.cx(1, 3)
qc.cx(1, 4)
qc.cx(2, 4)
qc.barrier()

qc.measure(3, 0)  # syndrome bit 1
qc.measure(4, 1)  # syndrome bit 2

# Step 3 (continued): Correction based on syndrome
with qc.if_test((qc.clbits[0], 1)):
    with qc.if_test((qc.clbits[1], 0)):
        qc.x(0)  # error on qubit 0

with qc.if_test((qc.clbits[0], 1)):
    with qc.if_test((qc.clbits[1], 1)):
        qc.x(1)  # error on qubit 1

with qc.if_test((qc.clbits[0], 0)):
    with qc.if_test((qc.clbits[1], 1)):
        qc.x(2)  # error on qubit 2

qc.barrier()
qc.measure(0, 2)  # final corrected readout of the logical qubit

print(qc.draw(output='text', fold=120))

# Step 4, 5, 6: Integrate, test, and run with the noise model
simulator = AerSimulator(noise_model=noise_model)
job = simulator.run(qc, shots=1024)
result = job.result()
counts = result.get_counts()

print("\nMeasurement counts (syndrome bits + corrected logical bit):")
print(counts)

# Step 7: OUTPUT
plot_histogram(counts, title="Error Correction Output (3-qubit bit-flip code)")
plt.tight_layout()
plt.savefig("assignment2_output.png", dpi=120)
print("\nHistogram saved as assignment2_output.png")