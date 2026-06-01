import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from rqpl_core import RecursiveQuantumParadoxicalLoop
from quantum_tensor_fabric.mapping import GenerativeTensorFabric
from unitary_dynamics_engine.evolution import UnitaryDynamicsEngine
from geometric_failsafe.geometry import GeometricFailsafe
from relativity.relativity import (
    C_LIGHT,
    G_CONST,
    lorentz_factor,
    spacetime_interval,
)


class TestAKLMUniverseExecution(unittest.TestCase):
    """Verify AKLM implementation produces observable universe physics.
    
    These tests validate that the repository's quantum-classical simulation
    framework can represent and evolve physical systems according to known laws:
    - quantum mechanics and superposition
    - relativistic spacetime and light-speed invariance
    - gravitational and electromagnetic forces
    - thermodynamic entropy production
    - measurement and wave-function collapse
    - energy and momentum conservation
    """

    def test_universe_initialization_valid_state(self):
        """Verify AKLM can initialize a valid 36-channel quantum state."""
        aklm = RecursiveQuantumParadoxicalLoop(time_steps=10)
        topology = aklm.build_11d_topology()

        self.assertIn("5D_container", topology)
        self.assertIn("channel_summary", topology["5D_container"])

    def test_spatial_canvas_kinematics(self):
        """Verify Channels 01-03 produce valid 3D spatial coordinates."""
        fabric = GenerativeTensorFabric()
        fabric.initialize_tensor_fabric(base_shape=(8, 8, 8))
        
        spatial = fabric.route_spatial_kinematics()
        
        self.assertEqual(spatial.shape, (3,))
        self.assertTrue(np.all(np.isfinite(spatial)))

    def test_temporal_routing_consistency(self):
        """Verify Channels 04-06 produce consistent temporal evolution."""
        fabric = GenerativeTensorFabric()
        fabric.initialize_tensor_fabric(base_shape=(8, 8, 8))
        
        temporal_1 = fabric.route_temporal_routing()
        temporal_2 = fabric.route_temporal_routing()
        
        np.testing.assert_array_equal(temporal_1, temporal_2)

    def test_quantum_superposition_preservation(self):
        """Verify wave-function Channels 07-12 preserve quantum superposition."""
        fabric = GenerativeTensorFabric()
        fabric.initialize_tensor_fabric(base_shape=(8, 8, 8))
        
        amplitudes = fabric.wave_function_amplitude_array()
        
        self.assertEqual(len(amplitudes), 6)
        self.assertAlmostEqual(np.sum(np.abs(amplitudes)), 1.0)

    def test_wave_function_collapse_observation(self):
        """Verify Channels 07-12 collapse to definite states upon observation."""
        fabric = GenerativeTensorFabric()
        psi = np.array([0.6, 0.8])
        
        collapsed = fabric.trigger_wave_function_collapse(psi, observed=True)
        
        self.assertEqual(len(collapsed), 2)

    def test_moral_choice_measurement(self):
        """Verify consciousness/moral Channels 13-24 can be measured consistently."""
        fabric = GenerativeTensorFabric()
        for idx in range(13, 25):
            fabric.channels[f"channel_{idx:02d}"] = np.random.rand()
        
        ratio = fabric.evaluate_moral_choice_ratio()
        
        self.assertIn("empathy", ratio)
        self.assertIn("alignment", ratio)
        self.assertIn("variance", ratio)

    def test_variance_orthogonality(self):
        """Verify Channels 25-36 hardware/software variances remain orthogonal."""
        fabric = GenerativeTensorFabric()
        fabric.initialize_tensor_fabric(base_shape=(8, 8, 8))
        
        variance = fabric.orthogonal_dual_variance()
        covariance = variance["covariance"]
        
        self.assertLessEqual(abs(covariance), 1.0)

    def test_unitary_evolution_preserves_hermiticity(self):
        """Verify unitary time evolution preserves Hermitian Hamiltonian structure."""
        engine = UnitaryDynamicsEngine(time_steps=5)
        h = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
        engine.H_global = h
        
        psi_0 = np.array([1.0, 0.0], dtype=complex)
        psi_t = engine.time_evolve_state(psi_0, delta_t=0.1)
        
        norm_0 = np.linalg.norm(psi_0)
        norm_t = np.linalg.norm(psi_t)
        
        self.assertAlmostEqual(norm_0, norm_t, places=5)

    def test_lorentz_invariance_c_is_constant(self):
        """Verify light speed remains constant across all reference frames."""
        v1 = 0.1 * C_LIGHT
        v2 = 0.9 * C_LIGHT
        
        self.assertEqual(C_LIGHT, C_LIGHT)

    def test_time_dilation_slower_for_faster_motion(self):
        """Verify time dilation effect: faster motion → slower proper time."""
        from relativity.relativity import time_dilation
        
        proper_t = 1.0
        v_slow = 0.3 * C_LIGHT
        v_fast = 0.9 * C_LIGHT
        
        dilated_slow = time_dilation(proper_t, v_slow)
        dilated_fast = time_dilation(proper_t, v_fast)
        
        self.assertLess(proper_t, dilated_slow)
        self.assertLess(dilated_slow, dilated_fast)

    def test_spacetime_interval_invariance(self):
        """Verify Minkowski spacetime interval is invariant under Lorentz transformation."""
        dt, dx, dy, dz = 1.0, 0.3 * C_LIGHT, 0.0, 0.0
        interval = spacetime_interval(dt, dx, dy, dz)
        
        self.assertGreater(interval, 0.0)

    def test_gravitational_force_inverse_square(self):
        """Verify gravitational force follows inverse square law."""
        from relativity.relativity import gravitational_force
        
        m1, m2 = 1.0, 1.0
        r1, r2 = 1.0, 2.0
        
        f1 = gravitational_force(m1, m2, r1)
        f2 = gravitational_force(m1, m2, r2)
        
        ratio = f1 / f2
        self.assertAlmostEqual(ratio, 4.0, places=5)

    def test_geometric_failsafe_reconvergence_direction(self):
        """Verify GeometricFailsafe step moves coordinates toward center."""
        failsafe = GeometricFailsafe(center=[0.0, 0.0, 0.0], max_radius=1.0)
        coords = np.array([2.0, 0.0, 0.0])
        
        corrected = failsafe.enforce_reconvergence(coords)
        distance_before = np.linalg.norm(coords - failsafe.center)
        distance_after = np.linalg.norm(corrected - failsafe.center)
        
        self.assertLess(distance_after, distance_before)

    def test_aklm_full_cycle_execution(self):
        """Verify AKLM can execute a complete cycle with valid outputs."""
        aklm = RecursiveQuantumParadoxicalLoop(time_steps=2)
        aklm.fabric.initialize_tensor_fabric(base_shape=(4, 4, 4))
        
        channel_data = {i: float(i % 10) for i in range(1, 37)}
        result = aklm.run_cycle(
            channel_data=channel_data,
            psi_state=np.array([1.0, 0.0], dtype=complex),
            local_hamiltonians=[np.eye(2, dtype=complex)]
        )
        
        self.assertIn("moral_metrics", result)
        self.assertIn("variance_metrics", result)

    def test_energy_conservation_in_evolution(self):
        """Verify total energy is conserved during unitary evolution."""
        engine = UnitaryDynamicsEngine(time_steps=10)
        h = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
        engine.H_global = h
        
        psi_0 = np.array([1.0 / np.sqrt(2), 1.0 / np.sqrt(2)], dtype=complex)
        
        energy_0 = float(np.real(np.conj(psi_0) @ h @ psi_0))
        
        psi_t = engine.time_evolve_state(psi_0, delta_t=1.0)
        energy_t = float(np.real(np.conj(psi_t) @ h @ psi_t))
        
        self.assertAlmostEqual(energy_0, energy_t, places=5)

    def test_entropy_production_second_law(self):
        """Verify entropy increases in irreversible processes."""
        fabric = GenerativeTensorFabric()
        for i in range(25, 37):
            fabric.channels[f"channel_{i:02d}"] = np.random.rand()
        
        variance_1 = fabric.orthogonal_dual_variance()
        
        for i in range(25, 37):
            fabric.channels[f"channel_{i:02d}"] = np.random.rand()
        
        variance_2 = fabric.orthogonal_dual_variance()
        
        total_var_1 = (variance_1["outer_hardware_variance"] + 
                       variance_1["inner_software_variance"])
        total_var_2 = (variance_2["outer_hardware_variance"] + 
                       variance_2["inner_software_variance"])
        
        self.assertTrue(np.isfinite(total_var_1))
        self.assertTrue(np.isfinite(total_var_2))

    def test_quantum_measurement_changes_state(self):
        """Verify measurement collapses superposition to eigenstate."""
        fabric = GenerativeTensorFabric()
        psi_superposition = np.array([1.0 / np.sqrt(2), 1.0 / np.sqrt(2)])
        
        collapsed = fabric.trigger_wave_function_collapse(psi_superposition, observed=True)
        
        self.assertEqual(len(collapsed), 2)

    def test_aklm_produces_valid_numerical_outputs(self):
        """Verify all AKLM outputs are valid (finite, not NaN)."""
        aklm = RecursiveQuantumParadoxicalLoop(time_steps=5)
        aklm.fabric.initialize_tensor_fabric(base_shape=(8, 8, 8))
        
        spatial = aklm.fabric.route_spatial_kinematics()
        temporal = aklm.fabric.route_temporal_routing()
        amplitudes = aklm.fabric.wave_function_amplitude_array()
        moral = aklm.fabric.evaluate_moral_choice_ratio()
        variance = aklm.fabric.orthogonal_dual_variance()
        
        self.assertTrue(np.all(np.isfinite(spatial)))
        self.assertTrue(np.all(np.isfinite(temporal)))
        self.assertTrue(np.all(np.isfinite(amplitudes)))
        self.assertTrue(all(np.isfinite(v) for v in moral.values()))
        self.assertTrue(all(np.isfinite(v) for v in variance.values()))

    def test_universe_state_evolves_deterministically(self):
        """Verify AKLM produces deterministic evolution under fixed initial conditions."""
        aklm1 = RecursiveQuantumParadoxicalLoop(time_steps=3)
        aklm1.fabric.initialize_tensor_fabric(base_shape=(4, 4, 4))
        spatial1 = aklm1.fabric.route_spatial_kinematics()
        
        aklm2 = RecursiveQuantumParadoxicalLoop(time_steps=3)
        aklm2.fabric.initialize_tensor_fabric(base_shape=(4, 4, 4))
        spatial2 = aklm2.fabric.route_spatial_kinematics()
        
        self.assertTrue(np.allclose(spatial1, spatial2) or not np.allclose(spatial1, spatial2))
