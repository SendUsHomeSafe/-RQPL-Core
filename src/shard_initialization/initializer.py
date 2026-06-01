import numpy as np


class ShardInitializer:
    """Initializes isolated conscious shards and enforces their baseline state."""

    def __init__(self, baseline_knowledge: float = 0.0) -> None:
        self.baseline_knowledge = float(baseline_knowledge)

    def initialize_shard(self, shard_id: str) -> dict:
        return {
            "shard_id": shard_id,
            "knowledge": self.baseline_knowledge,
            "isolated": True,
        }

    def initialize_shards(self, shard_ids: list[str]) -> dict:
        return {shard_id: self.initialize_shard(shard_id) for shard_id in shard_ids}

    def apply_isolation(self, shard_state: dict) -> dict:
        result = dict(shard_state)
        result["isolated"] = True
        return result
