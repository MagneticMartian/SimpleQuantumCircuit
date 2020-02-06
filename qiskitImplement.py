import qiskit as qk
from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
from qiskit import execute, Aer
from qiskit import IBMQ
from qiskit.tools.visualization import plot_histogram

secret_unitary = 'hz'

def apply_secret_unitary(secret_unitary, qubit, quantum_circuit, dagger):
    functionmap = {
        'x':quantum_circuit.x,
        'y':quantum_circuit.y,
        'z':quantum_circuit.z,
        'h':quantum_circuit.h,
        't':quantum_circuit.t,
        }
    if dagger: functionmap['t'] = quantum_circuit.tdg

    if dagger:
        [functionmap[unitary](qubit) for unitary in secret_unitary]
    else:
        [functionmap[unitary](qubit) for unitary in secret_unitary[::-1]]

#quantum circuit
q = QuantumRegister(3)
c = ClassicalRegister(3)
qc = QuantumCircuit(q, c)

apply_secret_unitary(secret_unitary, q[0], qc, dagger = 0)
qc.barrier()

#Entangled pair
qc.has_register(q[1])
qc.cx(q[1], q[2])
qc.barrier()

#teleportation protocol
qc.cx(q[0], q[1])
qc.h(q[0])
qc.measure(q[0], c[0])
qc.measure(q[1], c[1])
qc.cx(q[1], q[2])
qc.cz(q[0], q[2])
qc.barrier()

apply_secret_unitary(secret_unitary, q[2], qc, dagger=1)
qc.measure(q[2], c[2])

qc.draw(output='mpl')

backend = Aer.get_backend('qasm_simulator')
job_sim = execute(qc, backend, shots=1024)
sim_result = job_sim.result()

measurement_result = sim_result.get_counts(qc)
print(measurement_result)
plot_histogram(measurement_result)
