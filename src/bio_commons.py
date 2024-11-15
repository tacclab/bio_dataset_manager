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
