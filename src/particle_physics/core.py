import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class Particle:
    """Represents a fundamental particle in the AKLM tensor framework."""
    name: str
    particle_type: str  # quark, lepton, boson, higgs
    charge: float  # in units of elementary charge
    spin: float  # in units of ℏ
    mass_mev: float  # rest mass in MeV/c²
    lifetime_s: float  # decay lifetime in seconds (-1 for stable)
    flavor: str = ""
    
    def __repr__(self):
        return f"{self.name}(q={self.charge:+.2f}, m={self.mass_mev:.1f}MeV)"


class ParticlePhysics:
    """Maps AKLM tensor channels to Standard Model particles and processes."""
    
    # Physical constants
    PLANCK_LENGTH = 1.616e-35  # meters
    PLANCK_MASS = 2.176e-8  # kg
    PLANCK_TIME = 5.391e-44  # seconds
    PLANCK_TEMPERATURE = 1.417e32  # Kelvin
    
    SPEED_OF_LIGHT = 299792458.0  # m/s
    HBAR = 1.054571817e-34  # J·s
    G_NEWTON = 6.67430e-11  # m³/(kg·s²)
    
    # Elementary charge (MeV units)
    ELEMENTARY_CHARGE = 1.0
    
    def __init__(self):
        self.particles = self._initialize_standard_model()
        self.channel_map = self._create_channel_mapping()
    
    def _initialize_standard_model(self) -> Dict[str, Particle]:
        """Create all Standard Model particles."""
        particles = {}
        
        # Quarks (3 generations)
        quarks = [
            Particle("up", "quark", +2/3, 1/2, 2.16, -1, "first"),
            Particle("down", "quark", -1/3, 1/2, 4.67, -1, "first"),
            Particle("charm", "quark", +2/3, 1/2, 1275, -1, "second"),
            Particle("strange", "quark", -1/3, 1/2, 93.5, -1, "second"),
            Particle("top", "quark", +2/3, 1/2, 173210, -1, "third"),
            Particle("bottom", "quark", -1/3, 1/2, 4180, -1, "third"),
        ]
        
        # Leptons (3 generations)
        leptons = [
            Particle("electron", "lepton", -1.0, 1/2, 0.511, -1),
            Particle("electron_neutrino", "lepton", 0.0, 1/2, 0.0, -1),
            Particle("muon", "lepton", -1.0, 1/2, 105.7, 2.197e-6),
            Particle("muon_neutrino", "lepton", 0.0, 1/2, 0.0, -1),
            Particle("tau", "lepton", -1.0, 1/2, 1777, 2.693e-13),
            Particle("tau_neutrino", "lepton", 0.0, 1/2, 0.0, -1),
        ]
        
        # Gauge bosons
        bosons = [
            Particle("photon", "boson", 0.0, 1.0, 0.0, -1),
            Particle("W_plus", "boson", +1.0, 1.0, 80379, 3.157e-25),
            Particle("W_minus", "boson", -1.0, 1.0, 80379, 3.157e-25),
            Particle("Z_boson", "boson", 0.0, 1.0, 91188, 2.441e-25),
            Particle("gluon", "boson", 0.0, 1.0, 0.0, -1),
        ]
        
        # Higgs
        higgs = [
            Particle("Higgs", "higgs", 0.0, 0.0, 125100, 1.564e-22),
        ]
        
        for p in quarks + leptons + bosons + higgs:
            particles[p.name] = p
        
        return particles
    
    def _create_channel_mapping(self) -> Dict[str, Tuple[int, int]]:
        """Map AKLM 36 channels to particle physics domains."""
        return {
            "spatial_kinematics": (1, 3),       # x, y, z coordinates
            "temporal_energy": (4, 6),          # t, E, entropy
            "quantum_amplitudes": (7, 12),      # 6 quantum fields
            "quark_fields": (13, 18),           # 6 quark flavors
            "lepton_fields": (19, 24),          # 6 lepton types
            "gauge_fields": (25, 30),           # EM, weak, strong (3×2)
            "higgs_scalar": (31, 36),           # Higgs + scalar fields
        }
    
    def get_particle(self, name: str) -> Particle:
        """Retrieve particle by name."""
        return self.particles.get(name)
    
    def list_particles(self, particle_type: str = None) -> List[Particle]:
        """List particles, optionally filtered by type."""
        if particle_type is None:
            return list(self.particles.values())
        return [p for p in self.particles.values() if p.particle_type == particle_type]
    
    def tensor_to_particle_state(self, tensor_channels: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """Convert AKLM tensor channels to particle occupation numbers."""
        particle_state = {}
        
        quark_channels = tensor_channels.get("channel_13", np.zeros(6))
        lepton_channels = tensor_channels.get("channel_19", np.zeros(6))
        boson_channels = tensor_channels.get("channel_25", np.zeros(5))
        higgs_channels = tensor_channels.get("channel_31", np.zeros(1))
        
        quark_list = self.list_particles("quark")
        lepton_list = self.list_particles("lepton")
        boson_list = self.list_particles("boson")
        higgs_list = self.list_particles("higgs")
        
        for i, q in enumerate(quark_list):
            particle_state[q.name] = float(quark_channels.flat[i]) if i < len(quark_channels.flat) else 0.0
        
        for i, l in enumerate(lepton_list):
            particle_state[l.name] = float(lepton_channels.flat[i]) if i < len(lepton_channels.flat) else 0.0
        
        for i, b in enumerate(boson_list):
            particle_state[b.name] = float(boson_channels.flat[i]) if i < len(boson_channels.flat) else 0.0
        
        for i, h in enumerate(higgs_list):
            particle_state[h.name] = float(higgs_channels.flat[i]) if i < len(higgs_channels.flat) else 0.0
        
        return particle_state
    
    def big_bang_state(self, temperature_kelvin: float) -> Dict[str, float]:
        """Generate particle multiplicities at given temperature (Big Bang epoch)."""
        # At high T, all particles are populated according to Bose-Einstein or Fermi-Dirac
        # For simplicity: n_i ∝ (T/m_i)^(3/2) for massive particles
        
        multiplicities = {}
        k_b = 8.617333e-5  # Boltzmann constant in MeV/K
        temp_mev = k_b * temperature_kelvin
        
        for name, particle in self.particles.items():
            if particle.mass_mev == 0:
                multiplicities[name] = temp_mev ** 3
            else:
                if temp_mev > particle.mass_mev:
                    ratio = (temp_mev / particle.mass_mev) ** 1.5
                    multiplicities[name] = ratio * temp_mev
                else:
                    multiplicities[name] = 0.0
        
        return multiplicities
    
    def tensor_decompose_planck(self, tensor_elem: float, depth: int = 0, max_depth: int = 10) -> List[float]:
        """Recursively decompose tensor element to Planck scale.
        
        Binary tree decomposition: each element splits into 2^depth finer elements.
        At max_depth, each leaf represents Planck-scale quantum of energy/mass.
        """
        if depth >= max_depth:
            return [tensor_elem / (2 ** depth)]
        
        left = self.tensor_decompose_planck(tensor_elem / 2, depth + 1, max_depth)
        right = self.tensor_decompose_planck(tensor_elem / 2, depth + 1, max_depth)
        
        return left + right
    
    def estimate_particle_count_at_epoch(self, epoch_name: str, universe_volume_m3: float = 1.0) -> Dict[str, float]:
        """Estimate particle counts at each cosmological epoch."""
        epoch_params = {
            "planck_epoch": {"temp_k": 1.417e32, "duration_s": 5.391e-44},
            "gut_epoch": {"temp_k": 1e27, "duration_s": 1e-36},
            "inflation_epoch": {"temp_k": 1e27, "duration_s": 1e-32},
            "electroweak_epoch": {"temp_k": 1e15, "duration_s": 1e-12},
            "quark_epoch": {"temp_k": 1e12, "duration_s": 1e-6},
            "hadron_epoch": {"temp_k": 1e11, "duration_s": 1.0},
            "nucleosynthesis": {"temp_k": 1e9, "duration_s": 300.0},
            "recombination": {"temp_k": 3000, "duration_s": 380000 * 365.25 * 86400},
        }
        
        params = epoch_params.get(epoch_name, {})
        temp = params.get("temp_k", 1e9)
        
        multiplicities = self.big_bang_state(temp)
        
        scaled = {name: count * universe_volume_m3 for name, count in multiplicities.items()}
        
        return scaled


# Example usage functions
def diagnose_particle_physics_needs():
    """Run diagnostics to identify what's needed for AKLM particle physics."""
    pp = ParticlePhysics()
    
    print("=" * 70)
    print("PARTICLE PHYSICS DIAGNOSTIC FOR AKLM")
    print("=" * 70)
    
    print("\n1. STANDARD MODEL PARTICLES (18 fundamental types):")
    print(f"   Quarks: {len(pp.list_particles('quark'))}")
    print(f"   Leptons: {len(pp.list_particles('lepton'))}")
    print(f"   Bosons: {len(pp.list_particles('boson'))}")
    print(f"   Higgs: {len(pp.list_particles('higgs'))}")
    
    print("\n2. AKLM CHANNEL MAPPING:")
    for domain, (start, end) in pp.channel_map.items():
        print(f"   {domain}: channels {start:02d}-{end:02d}")
    
    print("\n3. PLANCK-SCALE DECOMPOSITION:")
    test_val = 1.0
    decomposed = pp.tensor_decompose_planck(test_val, max_depth=5)
    print(f"   Tensor element {test_val} → {len(decomposed)} Planck-scale quanta")
    print(f"   Each quantum: {decomposed[0]:.2e}")
    
    print("\n4. BIG BANG PARTICLE PRODUCTION:")
    epochs = ["planck_epoch", "gut_epoch", "electroweak_epoch", "nucleosynthesis"]
    for epoch in epochs:
        counts = pp.estimate_particle_count_at_epoch(epoch, universe_volume_m3=1e-105)
        photon_count = counts.get("photon", 0)
        electron_count = counts.get("electron", 0)
        print(f"   {epoch}: photons={photon_count:.1e}, electrons={electron_count:.1e}")
    
    print("\n5. MISSING IMPLEMENTATIONS:")
    print("   - Quantum field propagators (Feynman rules)")
    print("   - Perturbation theory (loop corrections)")
    print("   - Renormalization group flow")
    print("   - Hadronization cascade simulation")
    print("   - Thermal equilibrium solver")
    print("   - Cross-section calculator")
    print("   - Decay branching ratio resolver")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    diagnose_particle_physics_needs()
