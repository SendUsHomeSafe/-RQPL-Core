"""Lightweight hybrid training scaffold with hook support.

This trainer is framework-agnostic and intended as a scaffold: it runs a
configurable number of steps, calls hooks (callbacks), supports checkpointing,
and can integrate quantum or classical optimizers by passing `step_fn`.
"""
from __future__ import annotations

from typing import Any, Callable, Dict, Iterable, Optional
import time
import os
import json
import numpy as np


class Trainer:
    def __init__(self, model: Any, dataset: Iterable, out_dir: str = "./checkpoints"):
        self.model = model
        self.dataset = dataset
        self.out_dir = out_dir
        os.makedirs(self.out_dir, exist_ok=True)

    def run(self,
            epochs: int,
            steps_per_epoch: int,
            step_fn: Callable[[Any, Any], float],
            validate_fn: Optional[Callable[[Any], Dict[str, float]]] = None,
            callbacks: Optional[Dict[str, Callable[..., None]]] = None):
        """Run a simple training loop.

        - `step_fn(model, batch)` should perform a single optimization step and
          return a scalar loss (float).
        - `validate_fn(model)` returns a dict of metrics for validation.
        - `callbacks` can contain `on_step_end`, `on_epoch_end`, `on_checkpoint`.
        """
        callbacks = callbacks or {}
        on_step_end = callbacks.get("on_step_end")
        on_epoch_end = callbacks.get("on_epoch_end")
        on_checkpoint = callbacks.get("on_checkpoint")

        data_iter = iter(self.dataset)
        for epoch in range(1, epochs + 1):
            for step in range(1, steps_per_epoch + 1):
                try:
                    batch = next(data_iter)
                except StopIteration:
                    data_iter = iter(self.dataset)
                    batch = next(data_iter)

                loss = float(step_fn(self.model, batch))
                if on_step_end:
                    on_step_end(epoch=epoch, step=step, loss=loss)

            metrics = {}
            if validate_fn:
                metrics = validate_fn(self.model)
            if on_epoch_end:
                on_epoch_end(epoch=epoch, metrics=metrics)

            # checkpoint each epoch
            ckpt_path = os.path.join(self.out_dir, f"ckpt_epoch_{epoch}.npz")
            # save a lightweight snapshot of channels
            try:
                np.savez_compressed(ckpt_path, **{k: np.asarray(v).astype(float) for k, v in self.model.channels.items() if v is not None})
            except Exception:
                # fallback: write a small metadata file
                meta = {k: str(type(v)) for k, v in self.model.channels.items()}
                with open(ckpt_path + ".meta.json", "w") as f:
                    json.dump(meta, f)

            if on_checkpoint:
                on_checkpoint(epoch=epoch, path=ckpt_path)

        return True


__all__ = ["Trainer"]
