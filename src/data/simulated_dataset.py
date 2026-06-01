"""Small simulated dataset generator for AKLM training and tests.

Provides an iterable of small "clips" represented as dicts with `input` and `target`.
"""
from typing import Iterable, Dict
import numpy as np


def make_simulated_dataset(num_samples: int = 32, shape=(4, 4, 4)) -> Iterable[Dict[str, np.ndarray]]:
    rng = np.random.default_rng(42)
    for i in range(num_samples):
        clip = rng.uniform(0.0, 1.0, size=shape).astype(float)
        target = rng.uniform(0.0, 1.0, size=shape).astype(float)
        yield {"input": clip, "target": target}


__all__ = ["make_simulated_dataset"]
