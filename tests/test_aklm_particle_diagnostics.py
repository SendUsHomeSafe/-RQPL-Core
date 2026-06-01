import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from particle_physics.core import ParticlePhysics, diagnose_particle_physics_needs
from particle_physics.tensor_strategy import TensorDecompositionStrategy, print_training_plan


class TestAKLMParticlePhysicsMapping(unittest.TestCase):
    """Diagnostic tests for AKLM-to-particle-physics mapping."""
    
    def test_particle_physics_initialization(self):
        """Verify particle physics module initializes with full Standard Model."""
        pp = ParticlePhysics()
        
        self.assertEqual(len(pp.list_particles("quark")), 6)
        self.assertEqual(len(pp.list_particles("lepton")), 6)
        self.assertGreater(len(pp.list_particles("boson")), 0)
        self.assertEqual(len(pp.list_particles("higgs")), 1)
    
    def test_channel_mapping_coverage(self):
        """Verify AKLM 36 channels map to particle physics domains."""
        pp = ParticlePhysics()
        
        total_channels = sum(end - start + 1 for start, end in pp.channel_map.values())
        self.assertEqual(total_channels, 36)
    
    def test_planck_scale_decomposition(self):
        """Verify tensor decomposition reaches Planck scale."""
        pp = ParticlePhysics()
        
        tensor_val = 1.0
        decomposed = pp.tensor_decompose_planck(tensor_val, max_depth=10)
        
        self.assertEqual(len(decomposed), 2 ** 10)
        total = sum(decomposed)
        self.assertGreater(total, 0)
    
    def test_big_bang_particle_production(self):
        """Verify Big Bang tensor produces expected particle types."""
        pp = ParticlePhysics()
        
        planck_temp = 1.417e32  # Planck temperature
        multiplicities = pp.big_bang_state(planck_temp)
        
        self.assertIn("photon", multiplicities)
        self.assertIn("electron", multiplicities)
        self.assertIn("top", multiplicities)
        self.assertGreater(multiplicities["photon"], 0)
    
    def test_tensor_strategy_scale_hierarchy(self):
        """Verify scale hierarchy contains expected scales."""
        tds = TensorDecompositionStrategy()
        
        scales = tds.scale_hierarchy
        self.assertIn("planck", scales)
        self.assertIn("observable_universe", scales)
        self.assertGreater(scales["observable_universe"], scales["planck"])
    
    def test_tensor_strategy_depth_requirements(self):
        """Verify depth calculations for different physics scales."""
        tds = TensorDecompositionStrategy()
        
        depths = tds.required_depth_for_physics()
        
        self.assertLess(depths["classical_mechanics"], depths["atomic_physics"])
        self.assertLess(depths["atomic_physics"], depths["nuclear_physics"])
        self.assertLess(depths["nuclear_physics"], depths["quark_physics"])
        self.assertLess(depths["quark_physics"], depths["planck_scale"])
    
    def test_training_curriculum_stages(self):
        """Verify training curriculum has all stages."""
        tds = TensorDecompositionStrategy()
        
        curriculum = tds.training_curriculum()
        
        self.assertEqual(len(curriculum), 6)
        self.assertEqual(curriculum[0]["name"], "Cosmic Inflation")
        self.assertEqual(curriculum[-1]["name"], "Structure Formation")
    
    def test_memory_estimates_reasonable(self):
        """Verify memory estimates are physically reasonable."""
        tds = TensorDecompositionStrategy()
        
        memory = tds.memory_estimate_gb()
        
        # Planck scale should be largest
        planck_mem = [v for k, v in memory.items() if "planck" in k.lower()][0]
        atomic_mem = [v for k, v in memory.items() if "atomic" in k.lower()][0]
        
        self.assertGreater(planck_mem, atomic_mem)
    
    def test_epoch_particle_counts(self):
        """Verify particle counts at different cosmological epochs."""
        pp = ParticlePhysics()
        
        epochs_temps = {
            "planck_epoch": 1.417e32,
            "nucleosynthesis": 1e9,
            "recombination": 3000,
        }
        
        for epoch, temp in epochs_temps.items():
            counts = pp.estimate_particle_count_at_epoch(epoch)
            self.assertIn("photon", counts)
            self.assertGreater(counts["photon"], 0)


class TestAKLMImplementationNeeds(unittest.TestCase):
    """Document critical missing components for AKLM particle simulation."""
    
    MISSING_COMPONENTS = [
        "Quantum Field Propagator (Feynman rules for all 18 particles)",
        "Perturbation Theory Solver (QFT loop integrals)",
        "Renormalization Engine (running coupling evolution)",
        "Hadronization Simulator (quark fragmentation → hadrons)",
        "Thermal Equilibrium Solver (Bose-Einstein/Fermi-Dirac)",
        "Cross-section Calculator (2→N process amplitudes)",
        "Branching Ratio Resolver (particle decay modes)",
        "Spacetime Integrator (FLRW metric evolution)",
        "Inflation Engine (scalar field slow-roll)",
        "Nucleosynthesis Network (coupled nuclear reactions)",
    ]
    
    def test_document_missing_components(self):
        """Document all 10 missing components needed for Big Bang simulation."""
        self.assertEqual(len(self.MISSING_COMPONENTS), 10)
        
        # Each component has a clear purpose
        for component in self.MISSING_COMPONENTS:
            self.assertIn("(", component)
            self.assertIn(")", component)


def run_comprehensive_diagnostics():
    """Run all diagnostics and generate comprehensive report."""
    print("\n" + "=" * 90)
    print("COMPREHENSIVE AKLM PARTICLE PHYSICS DIAGNOSTICS")
    print("=" * 90)
    
    print("\n[1/2] PARTICLE PHYSICS MODULE DIAGNOSTICS:")
    print("-" * 90)
    diagnose_particle_physics_needs()
    
    print("\n[2/2] TRAINING & IMPLEMENTATION PLAN:")
    print("-" * 90)
    print_training_plan()
    
    print("\n" + "=" * 90)
    print("DIAGNOSTICS COMPLETE")
    print("=" * 90)


if __name__ == "__main__":
    # Run diagnostics by default
    import sys
    if len(sys.argv) == 1:
        run_comprehensive_diagnostics()
    else:
        unittest.main()
