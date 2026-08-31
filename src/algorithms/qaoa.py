from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
import networkx as nx

class QAOACircuitBuilder:
    """
    Constructs parameterized QAOA quantum circuits for Max-Cut problems.
    """
    def __init__(self, graph: nx.Graph, p: int = 1):
        self.graph = graph
        self.num_nodes = graph.number_of_nodes()
        self.edges = list(graph.edges())
        self.p = p

    def build_circuit(self) -> tuple[QuantumCircuit, ParameterVector, ParameterVector]:
        """
        Builds the full QAOA circuit with 'p' layers.
        
        Returns:
            qc: The parameterized QuantumCircuit.
            gammas: ParameterVector for Cost Layer parameters.
            betas: ParameterVector for Mixer Layer parameters.
        """
        qc = QuantumCircuit(self.num_nodes)

        # 1. Initialize qubits in equal superposition |+>
        qc.h(range(self.num_nodes))
        qc.barrier()

        # Define parameters
        gammas = ParameterVector('gamma', self.p)
        betas = ParameterVector('beta', self.p)

        # 2. Layer construction
        for layer in range(self.p):
            # --- Cost Layer U(C, gamma) ---
            for u, v in self.edges:
                qc.rzz(2 * gammas[layer], u, v)
            qc.barrier()

            # --- Mixer Layer U(B, beta) ---
            for i in range(self.num_nodes):
                qc.rx(2 * betas[layer], i)
            qc.barrier()

        # 3. Measurement
        qc.measure_all()

        return qc, gammas, betas