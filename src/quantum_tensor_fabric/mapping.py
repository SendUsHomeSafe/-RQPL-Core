import numpy as np
from typing import Any, Dict, Optional
from typing import List


class GenerativeTensorFabric:
    """
    Manages the 36-channel spatiotemporal tensor backend (AKLM).
    Handles the spatial canvas, temporal routing, unobserved wave-functions,
    moral telemetry, and orthogonal variance channels.
    """

    def __init__(self) -> None:
        self.channels: Dict[str, Any] = {
            f"channel_{i:02d}": None for i in range(1, 37)
        }
        self.observation_threshold: float = 1.0
        # registry for model blocks
        self.blocks: Dict[str, Any] = {}

    def _channel_vector(self, start: int, end: int) -> np.ndarray:
        values = []
        for i in range(start, end + 1):
            state = self.channels[f"channel_{i:02d}"]
            if state is None:
                values.append(0.0)
                continue
            array_state = np.asarray(state, dtype=float).ravel()
            values.append(float(array_state[0]) if array_state.size else 0.0)
        return np.asarray(values, dtype=float)

    def route_spatial_kinematics(self) -> np.ndarray:
        """Processes Channels 01-03 for the 3D execution canvas."""
        return self._channel_vector(1, 3)

    def route_temporal_routing(self) -> np.ndarray:
        """Processes Channels 04-06 for temporal routing and timeline embedding."""
        return self._channel_vector(4, 6)

    def wave_function_amplitude_array(self) -> np.ndarray:
        """Returns a normalized amplitude distribution for Channels 07-12."""
        amplitudes = self._channel_vector(7, 12)
        total = np.sum(np.abs(amplitudes))
        if total == 0.0:
            return np.full(amplitudes.shape, 1.0 / amplitudes.size)
        return amplitudes / total

    def evaluate_moral_choice_ratio(self) -> dict:
        """Summarizes Channels 13-24 into empathy, alignment, and variance metrics."""
        moral = self._channel_vector(13, 24)
        return {
            "empathy": float(np.mean(moral)),
            "alignment": float(np.median(moral)),
            "variance": float(np.var(moral)),
        }

    def orthogonal_dual_variance(self) -> dict:
        """Analyzes Channels 25-36 as orthogonal hardware and software variances."""
        environment = self._channel_vector(25, 30)
        intention = self._channel_vector(31, 36)
        covariance = float(np.cov(environment, intention)[0, 1]) if environment.size and intention.size else 0.0
        return {
            "outer_hardware_variance": float(np.var(environment)),
            "inner_software_variance": float(np.var(intention)),
            "covariance": covariance,
        }

    def initialize_tensor_fabric(self, base_shape: tuple = (32, 32, 32), dtype: np.dtype = np.float32) -> None:
        """Instantiate the 36-channel AKLM tensor fabric with safe defaults.

        Channels mapping:
        - 01-03: Spatial canvas (zeros)
        - 04-06: Temporal routing (ones)
        - 07-12: Wave-function amplitude samples (uniform [0,1])
        - 13-24: Moral choice ratio dataset (filled with 0.5)
        - 25-36: Orthogonal variance channels (small gaussian noise)
        """
        for i in range(1, 4):
            self.channels[f"channel_{i:02d}"] = np.zeros(base_shape, dtype=dtype)

        for i in range(4, 7):
            self.channels[f"channel_{i:02d}"] = np.ones(base_shape, dtype=dtype)

        for i in range(7, 13):
            self.channels[f"channel_{i:02d}"] = np.random.default_rng().uniform(0.0, 1.0, size=base_shape).astype(dtype)

        for i in range(13, 25):
            self.channels[f"channel_{i:02d}"] = np.full(base_shape, 0.5, dtype=dtype)

        for i in range(25, 37):
            # small variance around zero
            self.channels[f"channel_{i:02d}"] = np.random.default_rng().normal(0.0, 1e-4, size=base_shape).astype(dtype)

    def get_channel(self, idx: int) -> np.ndarray:
        """Return the ndarray for channel index `idx` (1-based). Raises KeyError if unset."""
        key = f"channel_{idx:02d}"
        arr = self.channels.get(key)
        if arr is None:
            raise KeyError(f"Channel {key} is not initialized")
        return np.asarray(arr)

    def collapse_at(self, coordinates: tuple[int, int, int], observed: bool, channel_from: int = 7) -> float:
        """Simulate a wave-function collapse at a given 3-tuple coordinate for Channels 07-12.

        If `observed` is True, sets the relevant channels at `coordinates` to
        `self.observation_threshold` and returns that certainty. If False, returns
        the fluid sample from `channel_07` at the coordinates.
        """
        x, y, z = coordinates
        if observed:
            for i in range(channel_from, channel_from + 6):
                key = f"channel_{i:02d}"
                if self.channels.get(key) is None:
                    # lazily initialize a scalar if missing
                    self.channels[key] = np.zeros((1, 1, 1), dtype=float)
                try:
                    self.channels[key][x, y, z] = self.observation_threshold
                except Exception:
                    # if coordinates are out of range, ignore the write and continue
                    pass
            return float(self.observation_threshold)

        # return fluid sample from channel_07 (if available)
        try:
            sample = self.get_channel(7)[x, y, z]
            return float(sample)
        except Exception:
            return 0.0

    # --- Block registry and pipeline -------------------------------------------------
    def register_block(self, name: str, block: Any) -> None:
        """Register a model block under `name`. The block must implement `process(channels)`."""
        self.blocks[name] = block

    def unregister_block(self, name: str) -> None:
        """Remove a registered block (no-op if missing)."""
        self.blocks.pop(name, None)

    def run_aklm_pipeline(self, order: Optional[List[str]] = None) -> Dict[str, np.ndarray]:
        """Run registered blocks in the given `order` (names). If `order` is None,
        runs blocks in insertion order. Each block's `process` receives the full
        `self.channels` mapping and should return a dict of channel updates.

        This pipeline realizes the manifest's 2D holographic conditional flow.
        Registered blocks compose the AKLM logic and perform the dual-variance
        transformations and moral stabilization updates that drive the system.
        Returns the final mapping of updates applied during this run.
        """
        updates: Dict[str, np.ndarray] = {}
        names = order if order is not None else list(self.blocks.keys())
        for name in names:
            block = self.blocks.get(name)
            if block is None:
                continue
            try:
                out = block.process(self.channels)
            except Exception:
                # be robust: skip failing blocks
                continue
            if not isinstance(out, dict):
                continue
            # apply updates in-place
            for k, v in out.items():
                self.channels[k] = v
                updates[k] = v
        return updates

    def trigger_wave_function_collapse(self, psi_state: np.ndarray, observed: bool) -> np.ndarray:
        """Collapses Channels 07-12 when observation occurs, otherwise leaves the state fluid.

        This method implements the manifest's local wave-function collapse behavior
        for the AKLM backend. Observation moves the quantum amplitude from a fluid
        probability state into a resolved, high-certainty channel representation.
        """
        psi = np.asarray(psi_state, dtype=complex)
        if observed:
            collapsed = np.full((psi.size,), self.observation_threshold, dtype=complex)
            return collapsed
        return psi

    def run_eqc_control(self, coordinates: tuple[int, int, int],
                        target_state: Optional[np.ndarray] = None,
                        feature_vector: Optional[np.ndarray] = None,
                        n_qubits: int = 4,
                        n_layers: int = 2,
                        noise_scale: float = 0.12,
                        schedule_step: float = 0.08,
                        decoherence_strength: float = 0.02) -> np.ndarray:
        """Run an EQC-enhanced control loop and update Channels 07-12.

        This method implements QCI-style EQC behavior:
        - Engineered Entropy: controlled vacuum fluctuation shaping.
        - Adaptive Scheduling: target-state back-correction.
        - Targeted Decoherence: internal whisper biasing.
        """
        try:
            from .quantum_integration import EQCAdapter
        except Exception:
            EQCAdapter = None  # type: ignore

        # prepare signal inputs
        if feature_vector is None:
            feature_vector = self._channel_vector(1, min(3, n_qubits))
        if target_state is None:
            target_state = self.wave_function_amplitude_array()

        if EQCAdapter is not None:
            eqc = EQCAdapter(n_qubits=n_qubits, n_layers=n_layers)
            eqc.build()
            entropy = eqc.engineered_entropy(feature_vector, noise_scale=noise_scale)
            schedule = eqc.adaptive_schedule(target_state, self.wave_function_amplitude_array(), step=schedule_step)
            decohered = eqc.targeted_decoherence(entropy, schedule, strength=decoherence_strength)
        else:
            decohered = np.full(6, 1.0 / 6.0)

        x, y, z = coordinates
        for i, val in enumerate(decohered, start=7):
            key = f"channel_{i:02d}"
            arr = self.channels.get(key)
            if arr is None:
                self.channels[key] = np.zeros((1, 1, 1), dtype=float)
                arr = self.channels[key]
            try:
                arr[x, y, z] = float(val)
            except Exception:
                try:
                    arr.flat[0] = float(val)
                except Exception:
                    pass

        # write a subtle moral bias signal into the first moral channel
        bias = float(np.mean(decohered))
        if self.channels.get("channel_13") is None:
            self.channels["channel_13"] = np.zeros((1, 1, 1), dtype=float)
        try:
            self.channels["channel_13"][0, 0, 0] = bias
        except Exception:
            self.channels["channel_13"].flat[0] = bias

        return np.asarray(decohered, dtype=float)

    def run_quantum_sampling(self, coordinates: tuple[int, int, int], feature_vector: Optional[np.ndarray] = None,
                             n_qubits: int = 4, n_layers: int = 2, use_eqc: bool = False) -> np.ndarray:
        """Run a small VQC or EQC-enhanced sampling to produce 6-channel outputs.

        This method implements the manifest's Counter-Current Engine sampling step.
        It uses `EQCAdapter` when `use_eqc=True`, otherwise the local `VQCAdapter`.
        Outputs are written into channels 07-12 at the provided coordinate.
        """
        if use_eqc:
            return self.run_eqc_control(
                coordinates,
                target_state=self.wave_function_amplitude_array(),
                feature_vector=feature_vector,
                n_qubits=n_qubits,
                n_layers=n_layers,
            )
        try:
            from .quantum_integration import VQCAdapter
        except Exception:
            VQCAdapter = None  # type: ignore

        # prepare feature vector
        if feature_vector is None:
            try:
                base = self.get_channel(1)
                # take a small slice and flatten to build features
                fv = np.ravel(base[0, :n_qubits, 0])[:n_qubits]
            except Exception:
                fv = np.zeros((n_qubits,), dtype=float)
        else:
            fv = np.asarray(feature_vector, dtype=float)

        if VQCAdapter is not None:
            adapter = VQCAdapter(n_qubits=n_qubits, n_layers=n_layers)
            adapter.build()
            outputs = adapter.run(fv)
        else:
            # fallback uniform output
            outputs = np.full(6, 1.0 / 6.0)

        # write outputs into channels 07-12 at the provided coordinate when possible
        x, y, z = coordinates
        for i, val in enumerate(outputs, start=7):
            key = f"channel_{i:02d}"
            arr = self.channels.get(key)
            if arr is None:
                # lazily create a scalar container
                self.channels[key] = np.zeros((1, 1, 1), dtype=float)
                arr = self.channels[key]
            try:
                arr[x, y, z] = float(val)
            except Exception:
                try:
                    arr.flat[0] = float(val)
                except Exception:
                    # give up if array isn't writable
                    pass

        return np.asarray(outputs, dtype=float)
