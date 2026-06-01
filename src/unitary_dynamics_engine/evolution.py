import numpy as np


class UnitaryDynamicsEngine:
    """
    Guides the simulation using pure unitary evolution over a closed global system.
    Utilizes amplitude amplification gates instead of dissipative non-Hermitian loss.
    """

    def __init__(self, time_steps: int) -> None:
        self.time_steps = time_steps
        self.H_global: np.ndarray | None = None

    def compile_global_hamiltonian(self, local_hamiltonians: list[np.ndarray]) -> np.ndarray:
        """Builds the global Hamiltonian from local temporal blocks using Kronecker products."""
        if not local_hamiltonians:
            raise ValueError("At least one local Hamiltonian is required.")

        global_matrix = np.asarray(local_hamiltonians[0], dtype=complex)
        for h_t in local_hamiltonians[1:]:
            global_matrix = np.kron(global_matrix, np.asarray(h_t, dtype=complex))

        self.H_global = global_matrix
        return self.H_global

    def execute_amplitude_amplification(self, timeline_vector: np.ndarray) -> np.ndarray:
        """Performs a reflection about the mean amplitude for constructive reinforcement."""
        timeline = np.asarray(timeline_vector, dtype=complex).ravel()
        if timeline.size == 0:
            return timeline

        average = np.mean(timeline)
        return 2 * average - timeline

    def time_evolve_state(self, psi_state: np.ndarray, delta_t: float = 1.0) -> np.ndarray:
        """Evolves the state vector under the current global Hamiltonian with a unitary operator."""
        if self.H_global is None:
            raise ValueError("Global Hamiltonian has not been compiled.")

        psi = np.asarray(psi_state, dtype=complex).ravel()
        if self.H_global.shape[0] != self.H_global.shape[1]:
            raise ValueError("Global Hamiltonian must be square.")
        if self.H_global.shape[0] != psi.size:
            raise ValueError("State vector dimension does not match Hamiltonian dimension.")

        eigenvalues, eigenvectors = np.linalg.eigh(self.H_global)
        evolution_operator = (
            eigenvectors
            @ np.diag(np.exp(-1j * eigenvalues * delta_t))
            @ eigenvectors.conj().T
        )
        return evolution_operator @ psi
