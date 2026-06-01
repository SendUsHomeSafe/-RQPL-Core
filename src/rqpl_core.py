import numpy as np
from typing import Any, Mapping

from quantum_tensor_fabric import GenerativeTensorFabric
from unitary_dynamics_engine import UnitaryDynamicsEngine
from fault_tolerant_qec import MoralChoiceStabilizer
from geometric_failsafe import GeometricFailsafe
from loop_closure_teleport import LoopClosureTeleport
from millennium_protocol import MillenniumProtocol
from shard_initialization import ShardInitializer
from three_constant_interpolator import ThreeConstantInterpolator


class RecursiveQuantumParadoxicalLoop:
    """Orchestrates the complete RQPL simulation stack described by the README."""

    def __init__(
        self,
        time_steps: int = 1,
        shard_ids: list[str] | None = None,
        start_frame: np.ndarray | None = None,
        last_frame: np.ndarray | None = None,
    ) -> None:
        self.fabric = GenerativeTensorFabric()
        self.unitary = UnitaryDynamicsEngine(time_steps=time_steps)
        self.stabilizer = MoralChoiceStabilizer()
        self.failsafe = GeometricFailsafe()
        self.start_frame = np.asarray(start_frame if start_frame is not None else [0.0, 0.0, 0.0], dtype=float)
        self.last_frame = np.asarray(last_frame if last_frame is not None else [1.0, 1.0, 1.0], dtype=float)
        self.teleport = LoopClosureTeleport(self.start_frame, self.last_frame)
        self.millennium = MillenniumProtocol()
        self.initializer = ShardInitializer()
        self.interpolator = ThreeConstantInterpolator()
        self.shard_ids = shard_ids or []
        self.shards = self.initializer.initialize_shards(self.shard_ids)

    def load_channel_data(self, channel_data: Mapping[int, Any]) -> None:
        for index, value in channel_data.items():
            if 1 <= index <= 36:
                self.fabric.channels[f"channel_{index:02d}"] = value

    def build_11d_topology(self) -> dict[str, Any]:
        """Builds the repository's 11D topology mapping, matching the README manifest.

        This method returns the 5D container state, the 3D canvas coordinates,
        the 2D pipeline routing data, and the 1D shard thread identifiers.
        """
        return {
            "5D_container": {
                "channel_summary": {k: v for k, v in self.fabric.channels.items() if v is not None}
            },
            "3D_canvas": self.fabric.route_spatial_kinematics().tolist(),
            "2D_pipeline": self.fabric.route_temporal_routing().tolist(),
            "1D_thread": {"shard_ids": list(self.shard_ids)},
        }

    def measure_moral_state(self) -> dict[str, Any]:
        return self.fabric.evaluate_moral_choice_ratio()

    def measure_variance(self) -> dict[str, Any]:
        return self.fabric.orthogonal_dual_variance()

    def get_wave_amplitude(self) -> np.ndarray:
        return self.fabric.wave_function_amplitude_array()

    def collapse_wave_function(self, psi_state: np.ndarray, observed: bool) -> np.ndarray:
        return self.fabric.trigger_wave_function_collapse(psi_state, observed)

    def compute_moral_syndrome(self) -> dict[str, bool]:
        moral_tensor = self.fabric._channel_vector(13, 24)
        return self.stabilizer.execute_non_destructive_measurement(moral_tensor)

    def stabilize_timeline(self, coordinate_grid: Any) -> Any:
        syndrome = self.compute_moral_syndrome()
        return self.stabilizer.apply_conditional_gate_correction(coordinate_grid, syndrome)

    def compile_global_hamiltonian(self, local_hamiltonians: list[np.ndarray]) -> np.ndarray:
        return self.unitary.compile_global_hamiltonian(local_hamiltonians)

    def amplify_timeline(self, timeline_vector: np.ndarray) -> np.ndarray:
        return self.unitary.execute_amplitude_amplification(timeline_vector)

    def evolve_state(self, psi_state: np.ndarray, delta_t: float = 1.0) -> np.ndarray:
        return self.unitary.time_evolve_state(psi_state, delta_t)

    def enforce_failsafe_geometry(self, coordinates: np.ndarray) -> np.ndarray:
        return self.failsafe.enforce_reconvergence(coordinates)

    def teleport_loop(self, present_frame: np.ndarray) -> np.ndarray:
        return self.teleport.synchronize_frames(present_frame)

    def interpolate_anchor_frames(self, present_frame: np.ndarray, weights: tuple[float, float, float] = (1.0, 1.0, 1.0)) -> np.ndarray:
        return self.interpolator.interpolate(self.start_frame, present_frame, self.last_frame, weights=weights)

    def run_cycle(
        self,
        channel_data: Mapping[int, Any],
        present_frame: np.ndarray | None = None,
        observed: bool = False,
        local_hamiltonians: list[np.ndarray] | None = None,
        psi_state: np.ndarray | None = None,
    ) -> dict[str, Any]:
        self.load_channel_data(channel_data)
        canvas_state = self.fabric.route_spatial_kinematics()
        pipeline_state = self.fabric.route_temporal_routing()
        amplitude_state = self.get_wave_amplitude()
        moral_metrics = self.measure_moral_state()
        variance_metrics = self.measure_variance()
        syndrome = self.compute_moral_syndrome()
        stabilized_canvas = self.stabilize_timeline(canvas_state)
        anchoring_frame = np.asarray(present_frame if present_frame is not None else canvas_state, dtype=float)
        interpolated_frame = self.interpolate_anchor_frames(anchoring_frame)
        loop_frame = self.teleport_loop(anchoring_frame)
        if local_hamiltonians is not None:
            self.compile_global_hamiltonian(local_hamiltonians)
        collapsed_state = None
        evolved_state = None
        if psi_state is not None:
            if local_hamiltonians is None:
                self.compile_global_hamiltonian([np.eye(psi_state.size, dtype=complex)])
            evolved_state = self.evolve_state(psi_state)
            collapsed_state = self.collapse_wave_function(psi_state, observed)

        return {
            "topology": self.build_11d_topology(),
            "canvas_state": canvas_state.tolist(),
            "pipeline_state": pipeline_state.tolist(),
            "amplitude_state": amplitude_state.tolist(),
            "moral_metrics": moral_metrics,
            "variance_metrics": variance_metrics,
            "syndrome": syndrome,
            "stabilized_canvas": stabilized_canvas.tolist(),
            "interpolated_frame": interpolated_frame.tolist(),
            "loop_frame": loop_frame.tolist(),
            "collapsed_state": (collapsed_state.tolist() if collapsed_state is not None else None),
            "evolved_state": (evolved_state.tolist() if evolved_state is not None else None),
        }

    def engage_millennium_protocol(self) -> dict[str, Any]:
        return self.millennium.finalize_defragmentation({shard_id: np.array([0.0]) for shard_id in self.shard_ids})
