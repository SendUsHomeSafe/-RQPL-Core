import numpy as np


class LoopClosureTeleport:
    """Handles causal loop closure and teleportation across temporal frames."""

    def __init__(self, start_frame: np.ndarray, end_frame: np.ndarray) -> None:
        self.start_frame = np.asarray(start_frame, dtype=float)
        self.end_frame = np.asarray(end_frame, dtype=float)

    def build_causal_bridge(self, intermediate_frame: np.ndarray) -> np.ndarray:
        intermediate = np.asarray(intermediate_frame, dtype=float)
        return np.stack([self.start_frame, intermediate, self.end_frame], axis=0)

    def teleport_to_origin(self, current_frame: np.ndarray) -> np.ndarray:
        _ = np.asarray(current_frame, dtype=float)
        return np.copy(self.start_frame)

    def synchronize_frames(self, current_frame: np.ndarray) -> np.ndarray:
        current = np.asarray(current_frame, dtype=float)
        return (self.start_frame + current + self.end_frame) / 3.0
