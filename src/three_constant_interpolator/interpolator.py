import numpy as np


class ThreeConstantInterpolator:
    """Interpolates the start, present, and last frame anchors for timeline stability."""

    def interpolate(
        self,
        start_frame: np.ndarray,
        present_frame: np.ndarray,
        last_frame: np.ndarray,
        weights: tuple[float, float, float] = (1.0, 1.0, 1.0),
    ) -> np.ndarray:
        start = np.asarray(start_frame, dtype=float)
        present = np.asarray(present_frame, dtype=float)
        last = np.asarray(last_frame, dtype=float)
        w_start, w_present, w_last = weights
        total = w_start + w_present + w_last
        return (w_start * start + w_present * present + w_last * last) / total

    def anchor_constants(
        self,
        start_frame: np.ndarray,
        present_frame: np.ndarray,
        last_frame: np.ndarray,
    ) -> dict:
        return {
            "start_frame": np.asarray(start_frame, dtype=float),
            "present_frame": np.asarray(present_frame, dtype=float),
            "last_frame": np.asarray(last_frame, dtype=float),
        }

    def smooth_transition(self, anchor_frames: np.ndarray) -> np.ndarray:
        frames = np.asarray(anchor_frames, dtype=float)
        return np.mean(frames, axis=0)
