import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from quantum_tensor_fabric.mapping import GenerativeTensorFabric
from unitary_dynamics_engine.evolution import UnitaryDynamicsEngine
from fault_tolerant_qec.stabilizer import MoralChoiceStabilizer
from geometric_failsafe import GeometricFailsafe
from loop_closure_teleport import LoopClosureTeleport
from millennium_protocol import MillenniumProtocol
from shard_initialization import ShardInitializer
from three_constant_interpolator import ThreeConstantInterpolator
from rqpl_core import RecursiveQuantumParadoxicalLoop


class TestGenerativeTensorFabric(unittest.TestCase):

    def test_route_spatial_kinematics_defaults(self):
        fabric = GenerativeTensorFabric()
        np.testing.assert_array_equal(fabric.route_spatial_kinematics(), np.zeros(3))

    def test_route_temporal_routing_defaults(self):
        fabric = GenerativeTensorFabric()
        np.testing.assert_array_equal(fabric.route_temporal_routing(), np.zeros(3))

    def test_wave_function_amplitude_array_default_distribution(self):
        fabric = GenerativeTensorFabric()
        amplitudes = fabric.wave_function_amplitude_array()
        np.testing.assert_array_almost_equal(amplitudes, np.full(6, 1.0 / 6.0))

    def test_evaluate_moral_choice_ratio(self):
        fabric = GenerativeTensorFabric()
        for idx in range(13, 25):
            fabric.channels[f"channel_{idx:02d}"] = idx % 2
        ratio = fabric.evaluate_moral_choice_ratio()

        self.assertIn("empathy", ratio)
        self.assertIn("variance", ratio)

    def test_orthogonal_dual_variance(self):
        fabric = GenerativeTensorFabric()
        for idx in range(25, 31):
            fabric.channels[f"channel_{idx:02d}"] = 0.5
        for idx in range(31, 37):
            fabric.channels[f"channel_{idx:02d}"] = 1.5
        variance = fabric.orthogonal_dual_variance()

        self.assertEqual(variance["covariance"], 0.0)

    def test_trigger_wave_function_collapse_unobserved(self):
        fabric = GenerativeTensorFabric()
        psi = np.array([0.2, 0.8])
        result = fabric.trigger_wave_function_collapse(psi, observed=False)

        np.testing.assert_array_equal(result, psi)

    def test_trigger_wave_function_collapse_observed(self):
        fabric = GenerativeTensorFabric()
        collapsed = fabric.trigger_wave_function_collapse(np.array([0.2, 0.8]), observed=True)

        np.testing.assert_array_equal(collapsed, np.array([1.0, 1.0], dtype=complex))


class TestMoralChoiceStabilizer(unittest.TestCase):

    def test_execute_non_destructive_measurement_no_error(self):
        stabilizer = MoralChoiceStabilizer(target_empathy_index=1.0)
        syndrome = stabilizer.execute_non_destructive_measurement([1.0, 1.0, 1.0])

        self.assertEqual(syndrome, {"bit_flip": False, "phase_flip": False})

    def test_execute_non_destructive_measurement_detects_phase_flip(self):
        stabilizer = MoralChoiceStabilizer(target_empathy_index=1.0)
        syndrome = stabilizer.execute_non_destructive_measurement([2.0, 2.0, 2.0])

        self.assertTrue(syndrome["phase_flip"])

    def test_apply_conditional_gate_correction_phase_flip(self):
        stabilizer = MoralChoiceStabilizer(target_empathy_index=1.0)
        syndrome = {"bit_flip": False, "phase_flip": True}
        corrected = stabilizer.apply_conditional_gate_correction(np.array([2.0, 2.0]), syndrome)

        np.testing.assert_allclose(corrected, np.array([1.9, 1.9]))


class TestUnitaryDynamicsEngine(unittest.TestCase):

    def test_compile_global_hamiltonian_kronecker(self):
        engine = UnitaryDynamicsEngine(time_steps=2)
        h1 = np.array([[1, 0], [0, -1]], dtype=complex)
        h2 = np.array([[0, 1], [1, 0]], dtype=complex)

        global_h = engine.compile_global_hamiltonian([h1, h2])
        expected = np.kron(h1, h2)

        np.testing.assert_array_equal(global_h, expected)
        self.assertIs(engine.H_global, global_h)

    def test_time_evolve_state_identity(self):
        engine = UnitaryDynamicsEngine(time_steps=1)
        engine.H_global = np.eye(2, dtype=complex)
        psi = np.array([1.0, 0.0], dtype=complex)

        evolved = engine.time_evolve_state(psi, delta_t=0.0)
        np.testing.assert_array_equal(evolved, psi)

    def test_execute_amplitude_amplification_reflection(self):
        engine = UnitaryDynamicsEngine(time_steps=1)
        vector = np.array([0.0, 1.0], dtype=complex)

        amplified = engine.execute_amplitude_amplification(vector)
        np.testing.assert_array_equal(amplified, np.array([1.0, 0.0], dtype=complex))

    def test_schrodinger_time_evolution_equation(self):
        engine = UnitaryDynamicsEngine(time_steps=1)
        h = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
        engine.H_global = h
        psi = np.array([1.0, 0.0], dtype=complex)

        evolved = engine.time_evolve_state(psi, delta_t=np.pi / 2)
        expected = np.exp(-1j * 1.0 * np.pi / 2) * psi

        np.testing.assert_allclose(evolved, expected)

    def test_documentation_includes_physics_equations(self):
        readme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "README.md"))
        with open(readme_path, "r", encoding="utf-8") as handle:
            contents = handle.read()

        self.assertIn("exp(-i H t)", contents)
        self.assertIn("H_global = H_1 ⊗ H_2", contents)
        self.assertIn("i d/dt |psi(t)> = H |psi(t)>", contents)


class TestGeometricFailsafe(unittest.TestCase):

    def test_evaluate_expansion(self):
        failsafe = GeometricFailsafe(center=[0.0, 0.0, 0.0], max_radius=2.0)
        radius = failsafe.evaluate_expansion(np.array([1.0, 0.0, 0.0]))

        self.assertAlmostEqual(radius, 1.0)

    def test_enforce_reconvergence(self):
        failsafe = GeometricFailsafe(center=[0.0, 0.0, 0.0], max_radius=2.0)
        corrected = failsafe.enforce_reconvergence(np.array([2.0, 0.0, 0.0]))

        self.assertLess(np.linalg.norm(corrected), 2.0)


class TestLoopClosureTeleport(unittest.TestCase):

    def test_build_causal_bridge(self):
        teleport = LoopClosureTeleport(np.array([0.0]), np.array([2.0]))
        bridge = teleport.build_causal_bridge(np.array([1.0]))

        np.testing.assert_array_equal(bridge, np.array([[0.0], [1.0], [2.0]]))

    def test_teleport_to_origin(self):
        teleport = LoopClosureTeleport(np.array([0.0]), np.array([2.0]))
        origin = teleport.teleport_to_origin(np.array([1.0]))

        np.testing.assert_array_equal(origin, np.array([0.0]))


class TestMillenniumProtocol(unittest.TestCase):

    def test_initialize_sandbox(self):
        protocol = MillenniumProtocol(sandbox_years=1000)
        sandbox = protocol.initialize_sandbox("shard-1")

        self.assertEqual(sandbox["shard_id"], "shard-1")
        self.assertEqual(sandbox["duration_years"], 1000)

    def test_spawn_isolated_vms(self):
        protocol = MillenniumProtocol()
        vms = protocol.spawn_isolated_vms(["shard-1"])

        self.assertIn("shard-1", vms)
        self.assertEqual(vms["shard-1"]["status"], "isolated")

    def test_finalize_defragmentation(self):
        protocol = MillenniumProtocol()
        merged = protocol.finalize_defragmentation({"shard-1": np.array([1.0, 3.0])})

        self.assertTrue(merged["closed"])
        self.assertEqual(merged["merged_states"]["shard-1"], 2.0)


class TestShardInitializer(unittest.TestCase):

    def test_initialize_shard(self):
        initializer = ShardInitializer(baseline_knowledge=0.0)
        shard = initializer.initialize_shard("shard-1")

        self.assertEqual(shard["shard_id"], "shard-1")
        self.assertTrue(shard["isolated"])

    def test_initialize_shards(self):
        initializer = ShardInitializer(baseline_knowledge=0.0)
        shards = initializer.initialize_shards(["shard-1", "shard-2"])

        self.assertEqual(len(shards), 2)


class TestThreeConstantInterpolator(unittest.TestCase):

    def test_interpolate(self):
        interpolator = ThreeConstantInterpolator()
        result = interpolator.interpolate(
            np.array([0.0]), np.array([1.0]), np.array([2.0])
        )

        np.testing.assert_array_equal(result, np.array([1.0]))

    def test_smooth_transition(self):
        interpolator = ThreeConstantInterpolator()
        frames = np.array([[0.0], [1.0], [2.0]])

        smoothed = interpolator.smooth_transition(frames)
        np.testing.assert_array_equal(smoothed, np.array([1.0]))


class TestRecursiveQuantumParadoxicalLoop(unittest.TestCase):

    def test_run_cycle_with_basic_input(self):
        core = RecursiveQuantumParadoxicalLoop(
            time_steps=1,
            shard_ids=["shard-1"],
            start_frame=np.array([0.0, 0.0, 0.0]),
            last_frame=np.array([2.0, 2.0, 2.0]),
        )
        channel_data = {1: 1.0, 2: 0.0, 3: 0.0, 25: 0.2, 31: 0.8}
        channel_data.update({idx: 1.0 for idx in range(13, 25)})
        result = core.run_cycle(
            channel_data=channel_data,
            present_frame=np.array([0.5, 0.5, 0.5]),
            observed=True,
            local_hamiltonians=[np.eye(2, dtype=complex)],
            psi_state=np.array([1.0, 0.0], dtype=complex),
        )

        self.assertIn("topology", result)
        self.assertEqual(result["moral_metrics"]["alignment"], 1.0)
        self.assertEqual(result["collapsed_state"], [1.0, 1.0])
        np.testing.assert_allclose(
            result["evolved_state"],
            [np.cos(1.0) - 1j * np.sin(1.0), 0.0],
        )


if __name__ == "__main__":
    unittest.main()
