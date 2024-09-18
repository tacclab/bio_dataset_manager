import os

import torch


def round_stat(stat: any, precision: int = 2) -> float:
    """
    Round a stat.
    :param stat: The stat to round.
    :param precision: The number of decimal places to round the stat to.
    :return: 
    """
    return round(stat, precision) if isinstance(stat, float) or isinstance(stat, int) else stat


def safe_ratio(x, y) -> float:
    """
    Safe ratio
    :param x:
    :param y:
    :return:
    """
    return 0 if x == 0 or y == 0 else min(x, y) / max(x, y)


def make_backup_folders(*folders) -> None:
    """
    Creates backup folders for the given list of folders.
    :param:*folders: Variable number of folder paths to be created.
    :return: None
    """
    [os.makedirs(folder, exist_ok=True) for folder in folders]


def apply_mask(out: torch.Tensor, lengths: torch.Tensor, is_oneway: bool = True) -> torch.Tensor:
    """
    Apply a mask to the input tensor based on the given lengths.

    :param out: The input tensor to be masked.
    :param lengths: The lengths of sequences in the input tensor.
    :param is_oneway: A boolean indicating whether to apply the mask in one direction or both. Default is True.

    :return: The masked output tensor.
    """
    # Check if the batch sizes of out and lengths match
    if lengths.size(0) != out.size(0):
        # If lengths contains only one element, repeat it for the whole batch
        if lengths.size(0) == 1:
            lengths = lengths.repeat(out.size(0))
        else:
            raise ValueError("Input and length tensors must have the same batch size.")
    # Create a mask based on sequence lengths
    mask = torch.arange(out.size(1)).expand(out.size(0), out.size(1)) < lengths.unsqueeze(1)
    mask = mask.unsqueeze(2).to(out.device)
    return out * mask.float() if is_oneway else out * mask.flip(dims=[1]).float()


def make_noise(num_samples: int, sequences_length: int, num_channels=1, device="cuda") -> torch.Tensor:
    """
    Create random noise samples of a specified shape and device.

    :param num_samples: The number of noise samples to create.
    :param sequences_length: The length of each sequence in the noise samples.
    :param num_channels: The number of channels for each sequence. Defaults to 1.
    :param device: The device to store the noise samples on. Defaults to "cuda".

    :return: torch.Tensor: Random noise samples with the specified shape and device.
    """
    noise_samples = torch.rand((num_samples, sequences_length, num_channels), device=device)
    return noise_samples


def efficient_zero_grad(model: torch.nn.Module) -> None:
    """
    Apply zero_grad more efficiently
    Source: https://betterprogramming.pub/how-to-make-your-pytorch-code-run-faster-93079f3c1f7b
    """
    for param in model.parameters():
        param.grad = None


@torch.no_grad()
def generate_new_sequences(generator: torch.nn.Module, num_samples: int, max_length: int,
                           sequences_lengths: torch.Tensor, noise_classes: int,
                           device: str = "cuda") -> torch.Tensor:
    """
    Generate new sequences using the provided generator.

    :param: generator: The generator model to use for generating sequences.
    :param: num_samples: The number of sequences to generate.
    :param: max_length: The maximum length of the generated sequences.
    :param: sequences_lengths: The length of each sequence to generate (is the noise_size).
    :param: device: The device to use for generating the sequences (default is "cuda").
    :param: noise_classes: The number of classes for the noise_classes
    :return: generated_sequences: The generated sequences.
    """
    if sequences_lengths is None:
        sequences_lengths = torch.tensor([max_length] * num_samples)

    if any(param is None for param in [num_samples, max_length, noise_classes]):
        raise ValueError("Error:num_samples, max_length and noise_classes must not be None")

    # Disable grad
    with torch.no_grad():
        noise_samples = make_noise(num_samples, max_length, noise_classes, device=device)
        generated_sequences = generator(noise_samples, lengths=sequences_lengths)
        return generated_sequences
