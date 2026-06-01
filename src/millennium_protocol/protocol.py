import numpy as np


class MillenniumProtocol:
    """Manages the Terminal Sandbox Phase and final defragmentation."""

    def __init__(self, sandbox_years: int = 1000) -> None:
        self.sandbox_years = int(sandbox_years)

    def initialize_sandbox(self, shard_id: str) -> dict:
        return {
            "shard_id": shard_id,
            "mode": "isolated",
            "duration_years": self.sandbox_years,
        }

    def spawn_isolated_vms(self, shard_ids: list[str]) -> dict:
        return {shard_id: {"status": "isolated", "active": True} for shard_id in shard_ids}

    def finalize_defragmentation(self, vm_states: dict[str, np.ndarray]) -> dict:
        merged = {
            shard_id: float(np.asarray(state, dtype=float).mean())
            if isinstance(state, np.ndarray)
            else float(state)
            for shard_id, state in vm_states.items()
        }
        return {"merged_states": merged, "closed": True}
