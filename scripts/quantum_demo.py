"""Small demo showing how to run the VQCAdapter and inject outputs into the AKLM fabric.

Run after installing dependencies listed in docs/QUANTUM.md.
"""
from pathlib import Path
import sys
import os
import numpy as np

# Ensure the package `src` is on path for local runs
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from quantum_tensor_fabric.quantum_integration import VQCAdapter
from quantum_tensor_fabric.mapping import GenerativeTensorFabric


def main() -> None:
    fabric = GenerativeTensorFabric()
    fabric.initialize_tensor_fabric(base_shape=(8, 8, 8))

    adapter = VQCAdapter(n_qubits=4, n_layers=2)
    adapter.build()

    # compress a small patch from channel_01 as a toy feature vector
    patch = fabric.get_channel(1)[0, :4, 0]
    features = patch.astype(float)

    outputs = adapter.run(features)
    print("VQC outputs (6, normalized):", outputs)

    # write outputs into channels 07-12 at coordinate (0,0,0)
    coord = (0, 0, 0)
    for i, val in enumerate(outputs, start=7):
        key = f"channel_{i:02d}"
        arr = fabric.channels[key]
        # broadcast scalar to arr if shapes mismatch for demo
        try:
            arr[coord] = val
        except Exception:
            arr.flat[0] = val

    print("Sample after injection:", [fabric.get_channel(i)[0, 0, 0] for i in range(7, 13)])


if __name__ == "__main__":
    main()
