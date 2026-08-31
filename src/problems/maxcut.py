import networkx as nx
import numpy as np

class MaxCutProblem:
    """
    Class representing the Max-Cut combinatorial optimization problem.
    Handles graph representation, cost functions, and bitstring evaluations.
    """
    def __init__(self, graph: nx.Graph):
        self.graph = graph
        self.num_nodes = graph.number_of_nodes()
        self.edges = list(graph.edges())

    def evaluate_bitstring(self, bitstring: str) -> float:
        """
        Calculates the Max-Cut value for a given binary string (e.g., '0110').
        Returns the total number of cut edges.
        """
        cut_value = 0.0
        for u, v in self.edges:
            if bitstring[u] != bitstring[v]:
                cut_value += 1.0
        return cut_value

    def get_state_costs(self) -> np.ndarray:
        """
        Generates the classical cost array for all 2^N state bitstrings.
        Useful for calculating exact expectations or brute-force verification.
        """
        num_states = 2 ** self.num_nodes
        costs = np.zeros(num_states)
        for i in range(num_states):
            bitstring = format(i, f'0{self.num_nodes}b')
            costs[i] = self.evaluate_bitstring(bitstring)
        return costs