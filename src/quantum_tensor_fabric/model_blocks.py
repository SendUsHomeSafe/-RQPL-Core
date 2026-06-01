"""Lightweight model block stubs for AKLM integration.

Each block implements a `process(channels: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]`
interface that accepts the current channel mapping and returns updates for one or more
channels. These are intentionally simple placeholders that can later be replaced with
real model code (wan2, flfv, i2v, inp, vace).
"""
from typing import Dict
import numpy as np


class BaseBlock:
    """Base class for model blocks."""

    def process(self, channels: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        raise NotImplementedError()


class Wan2(BaseBlock):
    """Spatial transformer stub that writes to channels 01-03."""

    def process(self, channels: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        out = {}
        # simple identity-copy of channel_01 into 01-03 scaled
        if "channel_01" in channels and channels["channel_01"] is not None:
            src = channels["channel_01"]
            for i in range(1, 4):
                out[f"channel_{i:02d}"] = np.copy(src) * (1.0 + (i - 1) * 0.01)
        return out


class FLFV(BaseBlock):
    """Temporal module stub for channels 04-06."""

    def process(self, channels: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        out = {}
        base = None
        for i in range(4, 7):
            key = f"channel_{i:02d}"
            if key in channels and channels[key] is not None:
                base = channels[key]
                break
        if base is None:
            base = np.zeros((1, 1, 1))
        for i in range(4, 7):
            out[f"channel_{i:02d}"] = base + 0.001 * i
        return out


class I2V(BaseBlock):
    """Image-to-video (i2v) stub that generates Channels 07-12 from inputs."""

    def process(self, channels: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        out = {}
        # create 07-12 as small random tensors seeded from channel_01
        seed = 0
        if "channel_01" in channels and channels["channel_01"] is not None:
            seed = int(np.sum(channels["channel_01"]) % 1000)
        rng = np.random.default_rng(seed)
        for i in range(7, 13):
            out[f"channel_{i:02d}"] = rng.uniform(0.0, 1.0, size=(1, 1, 1)).astype(float)
        return out


class INP(BaseBlock):
    """Interpolation/conditioning block that nudges channels 13-24."""

    def process(self, channels: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        out = {}
        for i in range(13, 25):
            key = f"channel_{i:02d}"
            arr = channels.get(key)
            if arr is None:
                out[key] = np.full((1, 1, 1), 0.5)
            else:
                out[key] = arr * 0.99 + 0.005
        return out


class VACE(BaseBlock):
    """Variance adjuster that operates on 25-36."""

    def process(self, channels: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        out = {}
        for i in range(25, 37):
            key = f"channel_{i:02d}"
            arr = channels.get(key)
            if arr is None:
                out[key] = np.zeros((1, 1, 1))
            else:
                out[key] = arr + np.mean(arr) * 1e-6
        return out


__all__ = ["Wan2", "FLFV", "I2V", "INP", "VACE", "BaseBlock"]
