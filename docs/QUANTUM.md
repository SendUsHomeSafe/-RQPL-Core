# Quantum integration for AKLM

This document describes a recommended path to integrate a small variational
quantum circuit (VQC) into the AKLM 36-channel tensor fabric.

1) Install recommended packages (simulator-first):

```bash
pip install --upgrade pip
pip install pennylane pennylane-qiskit qiskit numpy
```

2) Account setup for hardware (optional, recommended after prototyping):
- IBM Quantum: create an account at https://quantum-computing.ibm.com and follow the API key setup instructions. Use `pennylane-qiskit` or `qiskit` to target hardware.
- Rigetti / Braket / IonQ: follow each provider's registration flows.

3) Development workflow:
- Prototype VQC behavior locally using `scripts/quantum_demo.py`.
- Train/optimize VQC parameters using PennyLane optimizers on simulators.
- When ready, execute small evaluation jobs on IBM hardware to measure noise/latency.

4) Notes on qubit budgeting and best practices:
- Start with 4–8 qubits and shallow depth (1–3 layers).
- Use angle encoding for small feature vectors.
- Use many shots for statistical stability when executing on hardware.
- For QCI-style EQC, use `GenerativeTensorFabric.run_quantum_sampling(..., use_eqc=True)` or call `run_eqc_control()` directly.
- The `EQCAdapter` in `src/quantum_tensor_fabric/quantum_integration.py` implements engineered entropy, adaptive scheduling, and targeted decoherence.

See `src/quantum_tensor_fabric/quantum_integration.py` for the adapter implementation.
