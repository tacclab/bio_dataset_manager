import os
import random

import numpy as np
import torch
from Bio import SeqIO
from torch.nn.utils.rnn import pack_padded_sequence
from torch.utils.data import Dataset

from src.bio_sequences.bio_sequences_utils import BioSequencesUtils
from src.bio_sequences.dna_sequence import DnaSequence
from src.bio_sequences.protein_sequence import ProteinSequence


class BioDataset(Dataset):
    def __init__(
            self,
            dataset_folder: str or None,
            sequences: list or None,
            sequences_limit: int or None,
            randomize_choice: bool,
            pad_same_len: bool,
            window_size: int,
            sequence_info: ProteinSequence or DnaSequence,
    ) -> None:
        self.sequence_info = sequence_info
        self.sequence_utils = BioSequencesUtils(sequence_info)
        self.dataset_folder = dataset_folder
        self.sequences = sequences
        self.sequences_limit = sequences_limit
        self.randomize_choice = randomize_choice
        self.pad_same_len = pad_same_len
        self.window_size = window_size

        # Initialize the dataset
        self.char_to_index = {char: i for i, char in enumerate(self.sequence_info.charset)}
        self.index_to_char = {i: ch for i, ch in enumerate(self.sequence_info.charset)}
        self.num_classes = len(self.sequence_info.charset)

        self.init_dataset()

        self.avg_len = int(sum([len(seq) for seq in self.sequences]) / len(self.sequences)) if self.sequences else 0
        self.min_len = min([len(seq) for seq in self.sequences]) if self.sequences else 0
        self.max_len = max([len(seq) for seq in self.sequences]) if self.sequences else 0

    def init_dataset(self) -> None:
        if self.dataset_folder:
            self.sequences = self.load_sequences(self.dataset_folder)

        if not self.sequences:
            raise Exception("Sequences not found, specify the dataset folder or provide a list of sequences.")

        self.sequence_utils.filter_sequences(self.sequences, ["has_valid_start", "has_valid_stop", "has_valid_len"])

        if self.randomize_choice:
            random.shuffle(self.sequences)

        if self.sequences_limit:
            self.sequences = self.sequences[:self.sequences_limit]

        for sequence in self.sequences:
            if len(sequence) % self.window_size != 0:
                raise ValueError(f"Invalid window_size [{self.window_size}]"
                                 f", sequence length must be divisible by window size [{len(sequence)}]")

    def __len__(self) -> int:
        return len(self.sequences)

    def __getitem__(self, index: int) -> list or torch.Tensor:
        if self.pad_same_len:
            sequence_tensor = self.sequence_to_tensor(self.sequences[index])
            padded_sequence_tensor = self.pad_sequence(sequence_tensor)
            return padded_sequence_tensor
        return self.sequence_to_tensor(self.sequences[index])

    def load_sequences(self, dataset_folder: str) -> list:
        """
        Load the sequences from the dataset folder.
        :param dataset_folder:
        :return: list of sequences
        """
        self.sequences: list = []

        if dataset_folder is None:
            raise Warning("Dataset folder not specified.")

        for filename in os.listdir(dataset_folder):
            with open(os.path.join(dataset_folder, filename), "r") as file:
                data = [str(record.seq) for record in SeqIO.parse(file, "fasta")]
            self.sequences.extend(data)

        return self.sequences

    def tensor_to_sequence(self, sequence_tensor: torch.Tensor) -> str:
        """
        Convert a tensor to a sequence.
        :param sequence_tensor: Tensor of shape (num_groups, window_size * num_classes)
        :return: sequence (str)
        """
        sequence = []

        # Reshape tensor into (num_groups, window_size, num_classes)
        reshaped_tensor = sequence_tensor.view(-1, self.window_size, self.num_classes)

        for group in reshaped_tensor:
            for char_vec in group:
                # Get the index of the maximum value (one-hot encoding)
                char_index = torch.argmax(char_vec).item()
                # Convert index back to character and add to sequence
                sequence.append(self.index_to_char[char_index])

        return ''.join(sequence)

    def sequence_to_tensor(self, sequence: str) -> torch.Tensor:
        """
        Convert a sequence to a tensor.
        :param sequence: DNA or Protein sequence
        :return: tuple (sequence tensor, target tensor)
        """
        # Split sequence into groups of chars
        chars_groups = [sequence[i:i + self.window_size] for i in range(0, len(sequence), self.window_size)]
        one_hot_matrix = np.zeros((len(chars_groups), self.num_classes * self.window_size))

        for i, chars in enumerate(chars_groups):
            for j, char in enumerate(chars):
                one_hot_matrix[i, j * self.num_classes + self.char_to_index[char]] = 1.0

        tensor_seq = torch.tensor(one_hot_matrix, dtype=torch.float32)
        target = torch.tensor([self.char_to_index[char] for chars in chars_groups for char in chars], dtype=torch.long)
        return tensor_seq, target

    def pad_sequence(self, sequence_tensor: torch.Tensor) -> (torch.Tensor, None):
        """
        Pad a sequence tensor.
        :param sequence_tensor:
        :return: padded sequence tensor
        """

        target = None
        # Ensure sequence_tensor is actually a tensor. Assuming it's the first element of the tuple.
        if isinstance(sequence_tensor, tuple):
            sequence_tensor = sequence_tensor[0]

        # Verify sequence_tensor is a PyTorch tensor and has the method .size()
        if not hasattr(sequence_tensor, "size"):
            raise TypeError("sequence_tensor must be a PyTorch tensor")

        # Calculate the number of groups (windows) required to match the maximum sequence length
        num_groups = (self.max_len + self.window_size - 1) // self.window_size

        # Initialize the padded tensor with zeros
        padded_sequence = torch.zeros((num_groups, self.num_classes * self.window_size))

        # Copy the original sequence tensor into the padded tensor
        original_length = sequence_tensor.size(0)
        length_to_copy = min(original_length, num_groups)

        padded_sequence[:length_to_copy, :] = sequence_tensor[:length_to_copy, :]

        return padded_sequence, target

    @staticmethod
    def collate_fn(batch) -> (torch.Tensor, torch.Tensor):
        """
        Collate function for PyTorch DataLoader.
        :param batch:
        :return: packed inputs, targets
        """
        inputs, targets = zip(*batch)
        lengths = [len(seq) for seq in inputs]

        # Find the maximum length in the batch
        max_len = max(lengths)

        # Pad sequences to the maximum length
        padded_inputs = torch.zeros(len(inputs), max_len, inputs[0].shape[1])
        for i, seq in enumerate(inputs):
            padded_inputs[i, : len(seq), :] = seq

        # Convert to packed sequence
        packed_inputs = pack_padded_sequence(padded_inputs, lengths, batch_first=True, enforce_sorted=False)

        return packed_inputs, targets
