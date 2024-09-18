from pytest import fixture

from src.bio_dataset_manager.bio_dataset import BioDataset


@fixture
def bio_dataset_fixture(
        bio_sequences_fixture,
        sequence_info_fixture,
        window_size: int,
        pad_same_len: bool = False,
        randomize_choice: bool = False
) -> BioDataset:
    return BioDataset(
        dataset_folder=None,
        sequences=bio_sequences_fixture,
        sequences_limit=10,
        randomize_choice=randomize_choice,
        pad_same_len=pad_same_len,
        window_size=window_size,
        sequence_info=sequence_info_fixture
    )
