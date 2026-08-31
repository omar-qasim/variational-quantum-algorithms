import numpy as np
from scipy.optimize import minimize
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from src.problems.maxcut import MaxCutProblem

class QAOAOptimizer:
    """
    Handles the classical-quantum hybrid loop to optimize QAOA parameters (gamma, beta).
    """
    def __init__(self, problem: MaxCutProblem, circuit: QuantumCircuit, gammas, betas):
        self.problem = problem
        self.circuit = circuit
        self.gammas = gammas
        self.betas = betas
        self.sampler = StatevectorSampler()
        self.history = []

    def _cost_function(self, params: np.ndarray) -> float:
        p = len(self.gammas)
        gamma_vals = params[:p]
        beta_vals = params[p:]

        param_dict = {}
        for g_param, val in zip(self.gammas, gamma_vals):
            param_dict[g_param] = val
        for b_param, val in zip(self.betas, beta_vals):
            param_dict[b_param] = val

        bound_circuit = self.circuit.assign_parameters(param_dict)

        job = self.sampler.run([bound_circuit], shots=1024)
        result = job.result()[0]
        counts = result.data.meas.get_counts()

        total_shots = sum(counts.values())
        expectation = 0.0

        for bitstring, count in counts.items():
            cost = self.problem.evaluate_bitstring(bitstring)
            expectation += (count / total_shots) * cost

        # حفظ القيمة في الـ History
        self.history.append(expectation)

        return -expectation

    def optimize(self, initial_params: np.ndarray, method: str = 'COBYLA', maxiter: int = 100):
        self.history = []  # تصفير الـ History لكل تشغيل جديد
        res = minimize(
            self._cost_function,
            x0=initial_params,
            method=method,
            options={'maxiter': maxiter}
        )
        
        # إرجاع 3 قيم (الزوايا المثلى، أعلى Expectation، وقائمة التاريخ)
        return res.x, -res.fun, self.history