import numpy as np


class GeometricFailsafe:
    """Implements the outward-to-center failsafe geometry for the simulation."""

    def __init__(self, center: np.ndarray | list[float] = None, max_radius: float = 1.0) -> None:
        self.center = np.asarray(center if center is not None else [0.0, 0.0, 0.0], dtype=float)
        self.max_radius = float(max_radius)

    def evaluate_expansion(self, coordinates: np.ndarray) -> float:
        coords = np.asarray(coordinates, dtype=float).ravel()
        return float(np.linalg.norm(coords - self.center))

    def outward_expansion(self, coordinates: np.ndarray, scale: float = 1.0) -> np.ndarray:
        coords = np.asarray(coordinates, dtype=float)
        direction = coords - self.center
        return coords + direction * float(scale)

    def enforce_reconvergence(self, coordinates: np.ndarray) -> np.ndarray:
        coords = np.asarray(coordinates, dtype=float)
        direction = self.center - coords
        distance = np.linalg.norm(direction)
        if distance == 0:
            return coords
        step = direction / distance * min(distance, self.max_radius * 0.1)
        return coords + step
