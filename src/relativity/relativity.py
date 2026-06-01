import numpy as np

C_LIGHT = 299_792_458.0
G_CONST = 6.67430e-11


def lorentz_factor(v: float, c: float = C_LIGHT) -> float:
    """Return the Lorentz gamma factor for velocity v."""
    v = float(v)
    c = float(c)
    if abs(v) >= c:
        raise ValueError("Velocity must be less than the speed of light.")
    return float(1.0 / np.sqrt(1.0 - (v / c) ** 2))


def time_dilation(proper_time: float, v: float, c: float = C_LIGHT) -> float:
    """Return dilated time in the lab frame given proper time and velocity."""
    return float(proper_time * lorentz_factor(v, c))


def rest_energy(mass: float, c: float = C_LIGHT) -> float:
    """Return the rest energy E = m c^2."""
    return float(mass) * c ** 2


def relativistic_energy(mass: float, v: float, c: float = C_LIGHT) -> float:
    """Return total relativistic energy E = gamma m c^2."""
    return rest_energy(mass, c) * lorentz_factor(v, c)


def gravitational_force(m1: float, m2: float, distance: float, g: float = G_CONST) -> float:
    """Return Newtonian gravitational force F = G m1 m2 / r^2."""
    if distance <= 0:
        raise ValueError("Distance must be positive.")
    return float(g * m1 * m2 / distance ** 2)


def spacetime_interval(dt: float, dx: float, dy: float, dz: float, c: float = C_LIGHT) -> float:
    """Return the Minkowski spacetime interval ds^2 = c^2 dt^2 - dx^2 - dy^2 - dz^2."""
    return float((c * dt) ** 2 - dx ** 2 - dy ** 2 - dz ** 2)


def is_timelike_interval(dt: float, dx: float, dy: float, dz: float, c: float = C_LIGHT) -> bool:
    """Return True when the interval is timelike."""
    return spacetime_interval(dt, dx, dy, dz, c) > 0


def einstein_field_equation() -> str:
    """Return the canonical form of the Einstein field equations."""
    return "G_{μν} + Λ g_{μν} = 8 π T_{μν}"
