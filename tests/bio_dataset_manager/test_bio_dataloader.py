import pytest
import torch
import torch.multiprocessing as mp
from pytest import mark

from tests.commons import SequenceInfoTestType as Sit

# Ensure the 'spawn' method is used for multiprocessing
mp.set_start_method('spawn', force=True)


@mark.parametrize(
    "bio_sequences_fixture, sequence_info_fixture, window_size",
    [
        ((Sit.DNA, True), Sit.DNA, 1),
        ((Sit.PROTEIN, True), Sit.PROTEIN, 1),
        ((Sit.SMILES, True), Sit.SMILES, 1),
    ],
    indirect=["bio_sequences_fixture", "sequence_info_fixture"]
)
def test_bio_dataloader_init(bio_dataloader_fixture, bio_dataset_fixture, sequence_info_fixture, bio_sequences_fixture,
                             window_size):
    # Check if the dataloaders are created
    assert bio_dataloader_fixture.training_dataloader is not None
    assert bio_dataloader_fixture.validation_dataloader is not None


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
def test_split_dataset(bio_dataloader_fixture, bio_dataset_fixture, sequence_info_fixture, bio_sequences_fixture,
                       window_size):
    training_dataset, validation_dataset = bio_dataloader_fixture.split_dataset(bio_dataloader_fixture.split_ratio)

    # Check that the datasets have the correct sizes
    total_size = len(bio_dataloader_fixture.dataset)
    expected_validation_size = int(total_size * bio_dataloader_fixture.split_ratio)
    expected_training_size = total_size - expected_validation_size

    assert len(training_dataset) == expected_training_size
    assert len(validation_dataset) == expected_validation_size


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
@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA is not available")
def test_move_dataloader_to_gpu(bio_dataloader_fixture, bio_dataset_fixture, sequence_info_fixture,
                                bio_sequences_fixture,
                                window_size):
    # Use GPU for this test
    bio_dataloader_fixture.use_gpu = True
    bio_dataloader_fixture.init_dataloader(bio_dataloader_fixture.split_ratio)

    # Check if the dataloader has been moved to GPU
    for inputs, labels in bio_dataloader_fixture.training_dataloader:
        assert inputs.is_cuda  # Check if inputs are on the GPU


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
def test_create_dataloader(bio_dataloader_fixture, bio_dataset_fixture, sequence_info_fixture,
                           bio_sequences_fixture,
                           window_size):
    training_dataset, _ = bio_dataloader_fixture.split_dataset(bio_dataloader_fixture.split_ratio)
    dataloader_instance = bio_dataloader_fixture.create_dataloader(training_dataset, shuffle=True)

    # Check if the DataLoader has the correct batch size
    for batch in dataloader_instance:
        y_real, lengths = bio_dataloader_fixture.process_batch(batch, batch_first=True)
        assert len(lengths) == dataloader_instance.batch_size
        break


@mark.parametrize(
    "bio_sequences_fixture, sequence_info_fixture, window_size, use_gpu",
    [
        ((Sit.DNA, True), Sit.DNA, 1, False),
        ((Sit.DNA, True), Sit.DNA, 1, True),
        ((Sit.PROTEIN, True), Sit.PROTEIN, 1, False),
        ((Sit.PROTEIN, True), Sit.PROTEIN, 1, True),
        ((Sit.SMILES, True), Sit.SMILES, 1, True),

    ],
    indirect=["bio_sequences_fixture", "sequence_info_fixture"]
)
def test_dataloader_with_gpu_option(bio_dataloader_fixture, bio_dataset_fixture, sequence_info_fixture,
                                    bio_sequences_fixture, window_size, use_gpu):
    # Set the GPU option dynamically
    bio_dataloader_fixture.use_gpu = use_gpu
    bio_dataloader_fixture.init_dataloader(bio_dataloader_fixture.split_ratio)

    if use_gpu:
        for inputs, labels in bio_dataloader_fixture.training_dataloader:
            assert inputs.is_cuda  # Ensure tensors are moved to GPU
    else:
        for inputs, labels in bio_dataloader_fixture.training_dataloader:
            assert not inputs.is_cuda  # Ensure tensors are on CPU


if __name__ == '__main__':
    pytest.main()
