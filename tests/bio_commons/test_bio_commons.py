import os
import tempfile

import pytest
import torch

from src.bio_commons import round_stat, safe_ratio, make_backup_folders, apply_mask, efficient_zero_grad, make_noise, \
    generate_new_sequences


class DummyModel(torch.nn.Module):
    def __init__(self):
        super(DummyModel, self).__init__()
        self.fc = torch.nn.Linear(10, 10)

    def forward(self, x):
        return self.fc(x)


def test_round_stat():
    assert round_stat(3.14159) == 3.14
    assert round_stat(3.14159, 4) == 3.1416
    assert round_stat(3) == 3
    assert round_stat("string") == "string"
    assert round_stat(3.14159, 0) == 3


def test_safe_ratio():
    assert safe_ratio(5, 10) == 0.5
    assert safe_ratio(10, 5) == 0.5
    assert safe_ratio(0, 10) == 0
    assert safe_ratio(10, 0) == 0
    assert safe_ratio(0, 0) == 0


def test_make_backup_folders():
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        folder1 = os.path.join(tmpdir, "folder1")
        folder2 = os.path.join(tmpdir, "folder2")

        make_backup_folders(folder1, folder2)

        assert os.path.exists(folder1)
        assert os.path.exists(folder2)


def test_apply_mask():
    # Test case for is_oneway=True
    out = torch.randn(2, 5, 3)  # (batch_size, sequence_length, num_channels)
    lengths = torch.tensor([3, 5])
    masked_out = apply_mask(out, lengths, is_oneway=True)

    assert masked_out.size() == out.size()
    assert torch.all(masked_out[0, :3] == out[0, :3])  # First sequence, first 3 elements should be unchanged
    assert torch.all(masked_out[0, 3:] == 0)  # First sequence, elements after length should be zero
    assert torch.all(masked_out[1, :5] == out[1, :5])  # Second sequence, should match the original since length=5
    assert torch.all(masked_out[1, 5:] == 0)  # There should be no elements after length for the second sequence

    """
    # Test case for is_oneway=False
    masked_out_both = apply_mask(out, lengths, is_oneway=False)

    assert masked_out_both.size() == out.size()
    assert torch.all(masked_out_both[0, :3] == out[0, :3])  # First sequence, first 3 elements should be unchanged
    assert torch.all(masked_out_both[0, 3:] == 0)  # First sequence, elements after length should be zero
    assert torch.all(masked_out_both[1, :5] == out[1, :5])  # Second sequence, should match the original since length=5
    assert torch.all(masked_out_both[1, 5:] == 0)  # There should be no elements after length for the second sequence
    """


def test_make_noise():
    num_samples = 2
    sequences_length = 5
    num_channels = 3
    device = "cpu"  # You can change this to "cuda" if you have a GPU

    noise = make_noise(num_samples, sequences_length, num_channels, device=device)

    assert noise.size() == (num_samples, sequences_length, num_channels)
    assert noise.device.type == device


def test_efficient_zero_grad():
    model = DummyModel()
    for param in model.parameters():
        param.grad = torch.randn_like(param)

    efficient_zero_grad(model)

    for param in model.parameters():
        assert param.grad is None


def test_generate_new_sequences():
    class DummyGenerator(torch.nn.Module):
        def forward(self, x, lengths):
            return x  # For simplicity, just return the noise as the generated sequence

    generator = DummyGenerator()
    num_samples = 2
    max_length = 5
    sequences_lengths = torch.tensor([5, 5])
    noise_classes = 3
    device = "cpu"  # You can change this to "cuda" if you have a GPU

    generated_sequences = generate_new_sequences(generator, num_samples, max_length, sequences_lengths, noise_classes,
                                                 device=device)

    assert generated_sequences.size() == (num_samples, max_length, noise_classes)


if __name__ == "__main__":
    pytest.main()
