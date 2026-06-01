"""Quantum-attention prototype using VQCAdapter to compute attention weights.

This module defines a small `QuantumAttention` block compatible with the
`process(channels)` interface used by the AKLM pipeline blocks.
"""
from typing import Dict
import numpy as np

try:
    from .quantum_integration import VQCAdapter
    _HAS_VQC = True
except Exception:
    VQCAdapter = None  # type: ignore
    _HAS_VQC = False


class QuantumAttention:
    """Compute attention weights between two small feature vectors.

    Expects channels `channel_01` and `channel_02` to contain small feature
    vectors (or arrays where a small slice is taken). Returns updates for
    channels `channel_13` and `channel_14` as attention-weighted summaries.
    """

    def __init__(self, n_qubits: int = 4, n_layers: int = 2):
        self.n_qubits = n_qubits
        self.n_layers = n_layers
        self.adapter = None
        if _HAS_VQC:
            self.adapter = VQCAdapter(n_qubits=n_qubits, n_layers=n_layers)
            self.adapter.build()

    def _extract_vector(self, arr) -> np.ndarray:
        try:
            a = np.asarray(arr)
            flat = a.ravel()
            return flat[: self.n_qubits]
        except Exception:
            return np.zeros((self.n_qubits,))

    def process(self, channels: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        a = self._extract_vector(channels.get("channel_01"))
        b = self._extract_vector(channels.get("channel_02"))

        # simple classical fallback: cosine similarity-based weights if no VQC
        if not _HAS_VQC or self.adapter is None:
            # compute attention scalar and broadcast to small arrays
            denom = (np.linalg.norm(a) * np.linalg.norm(b)) if (np.linalg.norm(a) and np.linalg.norm(b)) else 1.0
            score = float(np.dot(a, b) / denom)
            w1 = 0.5 * (1 + score)
            w2 = 1.0 - w1
            out13 = np.full((1, 1, 1), w1, dtype=float)
            out14 = np.full((1, 1, 1), w2, dtype=float)
            return {"channel_13": out13, "channel_14": out14}

        # use VQC to compute 6-channel attention-like output and reduce
        raw = self.adapter.run(np.concatenate([a, b])[: self.n_qubits])
        # map first two entries to weights
        w = raw[:2]
        s = float(np.sum(w)) if float(np.sum(w)) != 0.0 else 1.0
        w_norm = w / s
        return {"channel_13": np.full((1, 1, 1), float(w_norm[0])), "channel_14": np.full((1, 1, 1), float(w_norm[1]))}


__all__ = ["QuantumAttention"]
