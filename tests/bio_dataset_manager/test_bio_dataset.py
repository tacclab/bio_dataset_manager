from pathlib import Path

import pytest
import torch
from pytest import mark

from src.bio_dataset_manager.bio_dataset import BioDataset
from tests.commons import PaddingLengthTestOptions
from tests.commons import SequenceInfoTestType as Sit
from tests.commons import TestDatasetFiles as Tdf


@mark.parametrize(
    "bio_sequences_fixture, sequence_info_fixture, window_size",
    [
        ((Sit.DNA, True), Sit.DNA, 1),
        ((Sit.DNA, True), Sit.DNA, 3),
        ((Sit.PROTEIN, True), Sit.PROTEIN, 1),
        ((Sit.SMILES, True), Sit.SMILES, 1),
    ],
    indirect=["bio_sequences_fixture", "sequence_info_fixture"]
)
def test_bio_dataset_initialization(bio_dataset_fixture, bio_sequences_fixture, sequence_info_fixture, window_size):
    assert bio_dataset_fixture.window_size == window_size
    assert bio_dataset_fixture.avg_len == int(
        sum(len(seq) for seq in bio_sequences_fixture) / len(bio_sequences_fixture)
    )


@mark.parametrize(
    "bio_sequences_fixture, sequence_info_fixture, window_size",
    [
        ((Sit.DNA, True), Sit.DNA, 1),
        ((Sit.DNA, True), Sit.DNA, 3),
        ((Sit.PROTEIN, True), Sit.PROTEIN, 1),
        ((Sit.SMILES, True), Sit.SMILES, 1),
    ],
    indirect=["bio_sequences_fixture", "sequence_info_fixture"]
)
def test_bio_dataset_tensor_to_sequence(bio_dataset_fixture, bio_sequences_fixture, sequence_info_fixture, window_size):
    for sequence in bio_sequences_fixture:
        bio_dataset_fixture.window_size = window_size
        tensor_seq, _ = bio_dataset_fixture.sequence_to_tensor(sequence)
        reconstructed_sequence = bio_dataset_fixture.tensor_to_sequence(tensor_seq)
        assert reconstructed_sequence == sequence


@mark.parametrize(
    "bio_sequences_fixture, sequence_info_fixture, window_size",
    [
        ((Sit.DNA, True), Sit.DNA, 1),
        ((Sit.PROTEIN, True), Sit.PROTEIN, 1),
        ((Sit.SMILES, True), Sit.SMILES, 1),
    ],
    indirect=["bio_sequences_fixture", "sequence_info_fixture"]
)
def test_bio_dataset_getitem(bio_dataset_fixture, bio_sequences_fixture, sequence_info_fixture, window_size):
    for i in range(len(bio_dataset_fixture)):
        tensor_seq, target = bio_dataset_fixture[i]
        assert isinstance(tensor_seq, torch.Tensor)
        assert isinstance(target, torch.Tensor)


@mark.parametrize(
    "bio_sequences_fixture, sequence_info_fixture, window_size",
    [
        ((Sit.DNA, True), Sit.DNA, 1),
        ((Sit.PROTEIN, True), Sit.PROTEIN, 1),
        ((Sit.SMILES, True), Sit.SMILES, 1),
    ],
    indirect=["bio_sequences_fixture", "sequence_info_fixture"]
)
def test_bio_dataset_tensor_to_sequence(bio_dataset_fixture, bio_sequences_fixture, sequence_info_fixture, window_size):
    for sequence in bio_sequences_fixture:
        bio_dataset_fixture.window_size = window_size
        tensor_seq, _ = bio_dataset_fixture.sequence_to_tensor(sequence)
        reconstructed_sequence = bio_dataset_fixture.tensor_to_sequence(tensor_seq)
        assert reconstructed_sequence == sequence


@mark.parametrize(
    "sequence_info_fixture, file_path, window_size, sequences_limit",
    [
        (Sit.DNA, Path(Tdf.dna_test_dataset_file), 1, 2),
        (Sit.PROTEIN, Path(Tdf.protein_test_dataset_file), 1, 2),
        (Sit.SMILES, Path(Tdf.smiles_test_dataset_file), 1, 2),
    ],
    indirect=["sequence_info_fixture"]
)
def test_load_from_file(sequence_info_fixture, file_path, window_size, sequences_limit):
    dataset_path = file_path.parent
    bio_dataset = BioDataset(
        dataset_folder=dataset_path,
        sequences=None,
        sequences_limit=sequences_limit,
        randomize_choice=False,
        pad_same_len=False,
        window_size=window_size,
        sequence_info=sequence_info_fixture
    )
    assert len(bio_dataset) == sequences_limit


@mark.parametrize(
    "bio_sequences_fixture, sequence_info_fixture, window_size, pad_length",
    [
        ((Sit.DNA, True), Sit.DNA, 3, PaddingLengthTestOptions.SAME),
        ((Sit.PROTEIN, True), Sit.PROTEIN, 1, PaddingLengthTestOptions.SAME),
        ((Sit.DNA, True), Sit.DNA, 3, PaddingLengthTestOptions.LONGER),
        ((Sit.PROTEIN, True), Sit.PROTEIN, 1, PaddingLengthTestOptions.LONGER),
        ((Sit.SMILES, True), Sit.SMILES, 1, PaddingLengthTestOptions.LONGER),
    ],
    indirect=["bio_sequences_fixture", "sequence_info_fixture"]
)
def test_pad_sequence_same_length(bio_dataset_fixture, bio_sequences_fixture, sequence_info_fixture, window_size,
                                  pad_length):
    for sequence in bio_sequences_fixture:
        if PaddingLengthTestOptions.SAME == pad_length:
            bio_dataset_fixture.max_len = len(sequence)
        if PaddingLengthTestOptions.LONGER == pad_length:
            bio_dataset_fixture.max_len = len(sequence) + window_size

        sequence_tensor, _ = bio_dataset_fixture.sequence_to_tensor(sequence)
        padded_sequence, target = bio_dataset_fixture.pad_sequence(sequence_tensor)

        # Verify that the shape of the padded sequence matches the expected shape
        expected_shape = (bio_dataset_fixture.max_len // window_size, window_size * len(sequence_info_fixture.charset))
        assert padded_sequence.shape == expected_shape

        # Verify that the first part of the padded sequence matches the original sequence tensor
        original_sequence_length = sequence_tensor.shape[0]
        assert torch.all(padded_sequence[:original_sequence_length] == sequence_tensor)


if __name__ == "__main__":
    pytest.main()
