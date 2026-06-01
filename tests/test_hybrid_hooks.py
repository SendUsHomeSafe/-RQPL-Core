import os
import tempfile
import numpy as np

from training.hybrid_trainer import Trainer
from data.simulated_dataset import make_simulated_dataset
from quantum_tensor_fabric.mapping import GenerativeTensorFabric
from quantum_tensor_fabric.quantum_attention import QuantumAttention


def test_trainer_runs_and_hooks(tmp_path):
    # prepare model and dataset
    fabric = GenerativeTensorFabric()
    fabric.initialize_tensor_fabric(base_shape=(2, 2, 2))

    dataset = list(make_simulated_dataset(num_samples=4, shape=(2, 2, 2)))

    # simple step function: write input mean into channel_01 and return loss
    def step_fn(model, batch):
        val = float(np.mean(batch["input"]))
        model.channels["channel_01"] = np.full((2, 2, 2), val)
        # loss as difference to target mean
        return abs(val - float(np.mean(batch["target"])))

    # validation function
    def validate_fn(model):
        return {"coverage": 1.0}

    events = {"steps": 0, "epochs": 0}

    def on_step_end(**kwargs):
        events["steps"] += 1

    def on_epoch_end(**kwargs):
        events["epochs"] += 1

    out_dir = tmp_path / "ckpts"
    trainer = Trainer(fabric, dataset, out_dir=str(out_dir))
    ok = trainer.run(epochs=2, steps_per_epoch=2, step_fn=step_fn, validate_fn=validate_fn,
                     callbacks={"on_step_end": on_step_end, "on_epoch_end": on_epoch_end})

    assert ok is True
    assert events["steps"] == 4
    assert events["epochs"] == 2
    # check checkpoints exist
    files = list(out_dir.glob("ckpt_epoch_*.npz"))
    assert len(files) == 2


def test_quantum_attention_block_and_pipeline():
    fabric = GenerativeTensorFabric()
    fabric.initialize_tensor_fabric(base_shape=(2, 2, 2))

    # seed small vectors
    fabric.channels["channel_01"] = np.full((2, 2, 2), 0.2)
    fabric.channels["channel_02"] = np.full((2, 2, 2), 0.4)

    qa = QuantumAttention(n_qubits=4, n_layers=1)
    # register block and run pipeline
    fabric.register_block("quantum_attn", qa)
    updates = fabric.run_aklm_pipeline(order=["quantum_attn"])

    assert "channel_13" in updates and "channel_14" in updates
    c13 = float(np.asarray(updates["channel_13"]).ravel()[0])
    c14 = float(np.asarray(updates["channel_14"]).ravel()[0])
    # weights should sum approximately to 1
    assert abs((c13 + c14) - 1.0) < 1e-6


def test_eqc_control_loop_updates_wave_function_state():
    fabric = GenerativeTensorFabric()
    fabric.initialize_tensor_fabric(base_shape=(2, 2, 2))

    # initial channel state and target wave amplitude
    fabric.channels["channel_01"] = np.full((2, 2, 2), 0.3)
    decohered = fabric.run_eqc_control(coordinates=(0, 0, 0), n_qubits=4, n_layers=1)

    assert isinstance(decohered, np.ndarray)
    assert decohered.shape == (6,)
    assert abs(np.sum(decohered) - 1.0) < 1e-6
    assert np.all(np.asarray(fabric.channels["channel_07"]).flat[0] >= 0.0)
