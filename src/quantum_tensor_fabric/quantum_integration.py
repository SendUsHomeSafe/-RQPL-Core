"""Quantum integration helpers for AKLM.

Provides a small VQC adapter that returns 6-channel outputs usable for
channels 07-12. Uses PennyLane when available, otherwise falls back to a
deterministic pseudo-quantum simulator (numpy-based) so the code is import-safe.

This module is intentionally minimal and designed for local simulator-first
development. See docs/QUANTUM.md for hardware setup and provider instructions.
"""
from __future__ import annotations

from typing import Iterable, Optional
import numpy as np

try:
    import pennylane as qml  # type: ignore
    from pennylane import numpy as pnp  # type: ignore
    _HAS_PENNY = True
except Exception:
    qml = None  # type: ignore
    pnp = np  # type: ignore
    _HAS_PENNY = False


class VQCAdapter:
    """Adapter for a small variational quantum circuit producing 6 outputs.

    Usage:
        adapter = VQCAdapter(n_qubits=4, n_layers=2)
        adapter.build()  # builds circuit for PennyLane if available
        out = adapter.run(np.array([0.1, 0.2, 0.3, 0.4]))  # length <= n_qubits
    """

    def __init__(self, n_qubits: int = 4, n_layers: int = 2, seed: Optional[int] = 42):
        self.n_qubits = int(n_qubits)
        self.n_layers = int(n_layers)
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self._built = False

    def build(self) -> None:
        if not _HAS_PENNY:
            self._built = True
            return

        dev = qml.device("default.qubit", wires=self.n_qubits)

        @qml.qnode(dev, interface="autograd")
        def circuit(params, x):
            # angle-encode up to n_qubits features
            for i in range(min(len(x), self.n_qubits)):
                qml.RY(float(x[i]), wires=i)

            # variational layers
            idx = 0
            for l in range(self.n_layers):
                for q in range(self.n_qubits):
                    qml.RY(params[idx], wires=q)
                    idx += 1
                for q in range(self.n_qubits - 1):
                    qml.CNOT(wires=[q, q + 1])

            # return expectation values (pad/repeat to get 6 outputs)
            exps = [qml.expval(qml.PauliZ(wires=i % self.n_qubits)) for i in range(6)]
            return exps

        # initialize params
        n_params = self.n_layers * self.n_qubits
        init = self.rng.normal(0.0, 0.1, size=(n_params,))

        self._circuit = circuit
        self._params = pnp.array(init) if _HAS_PENNY else init
        self._built = True

    def run(self, x: Iterable[float]) -> np.ndarray:
        """Run the VQC (or fallback) and return 6 outputs mapped to [0,1]."""
        if not self._built:
            self.build()

        x_arr = np.asarray(list(x), dtype=float)

        if _HAS_PENNY:
            raw = np.asarray(self._circuit(self._params, x_arr), dtype=float)
        else:
            # fallback: deterministic pseudo-quantum mapping using trigonometric features
            phases = np.sin(x_arr[: self.n_qubits] + np.arange(self.n_qubits))
            raw = np.zeros(6)
            for i in range(6):
                raw[i] = np.tanh(np.sum(phases) * (i + 1) * 0.1)

        # map from [-1,1] -> [0,1]
        mapped = (raw + 1.0) / 2.0
        # normalize to make a probability-like vector
        s = np.sum(mapped)
        if s == 0:
            return np.full(6, 1.0 / 6.0)
        return mapped / s


class EQCAdapter:
    """Adaptive Entropy Quantum Computing (EQC) adapter for engineered entropy.

    This class implements the QCI-style EQC concepts:
    - Engineered Entropy: controlled vacuum-fluctuation noise shaping.
    - Adaptive Scheduling: backward-corrected target updates.
    - Targeted Decoherence: subtle internal biasing of channel states.
    """

    def __init__(self, n_qubits: int = 4, n_layers: int = 2, seed: Optional[int] = 1234):
        self.n_qubits = int(n_qubits)
        self.n_layers = int(n_layers)
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.vqc = VQCAdapter(n_qubits=n_qubits, n_layers=n_layers, seed=seed)
        self._built = False

    def build(self) -> None:
        self.vqc.build()
        self._built = True

    def engineered_entropy(self, feature_vector: np.ndarray, noise_scale: float = 0.12) -> np.ndarray:
        """Produce controlled randomness by shaping vacuum fluctuation noise."""
        base = np.asarray(feature_vector, dtype=float)
        if base.size < self.n_qubits:
            base = np.pad(base, (0, max(0, self.n_qubits - base.size)), constant_values=0.0)
        base = base[: self.n_qubits]

        amplitudes = self.vqc.run(base)
        vacuum = self.rng.normal(0.0, noise_scale, size=amplitudes.shape)
        shaped = np.clip(amplitudes + vacuum, 0.0, 1.0)
        total = np.sum(shaped)
        return shaped / total if total != 0.0 else np.full_like(shaped, 1.0 / shaped.size)

    def adaptive_schedule(self, target_state: np.ndarray, current_state: np.ndarray, step: float = 0.08) -> np.ndarray:
        """Work backward from a desired target state to correct the current state."""
        target = np.asarray(target_state, dtype=float)
        current = np.asarray(current_state, dtype=float)

        if target.size < 6:
            target = np.pad(target, (0, 6 - target.size), constant_values=0.0)
        if current.size < 6:
            current = np.pad(current, (0, 6 - current.size), constant_values=0.0)

        corrected = current + step * (target - current)
        corrected = np.clip(corrected, 0.0, 1.0)
        total = float(np.sum(corrected))
        return corrected / total if total != 0.0 else np.full(6, 1.0 / 6.0)

    def targeted_decoherence(self, channel_state: np.ndarray, influence_vector: np.ndarray, strength: float = 0.02) -> np.ndarray:
        """Apply subtle decoherence bias as an internal whisper rather than a command."""
        state = np.asarray(channel_state, dtype=float)
        influence = np.asarray(influence_vector, dtype=float)

        if influence.size < state.size:
            influence = np.pad(influence, (0, state.size - influence.size), constant_values=0.0)
        if state.size < influence.size:
            state = np.pad(state, (0, influence.size - state.size), constant_values=0.0)

        perturbed = state + strength * (influence[: state.size] - state)
        perturbed = np.clip(perturbed, 0.0, 1.0)
        total = float(np.sum(perturbed))
        return perturbed / total if total != 0.0 else np.full(state.shape, 1.0 / state.size)


__all__ = ["VQCAdapter", "EQCAdapter"]
