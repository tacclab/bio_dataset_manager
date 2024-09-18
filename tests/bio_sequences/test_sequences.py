import pytest
from pytest import mark

from src.bio_sequences.bio_sequences_config import DnaSequenceConfig, ProteinSequenceConfig, SmilesSequenceConfig
from tests.commons import SequenceInfoTestType as Sit
from tests.commons import TestDatasetFiles as Tdf


@mark.parametrize(
    "sequence_info_fixture, expected_config",
    [(Sit.DNA, DnaSequenceConfig), (Sit.PROTEIN, ProteinSequenceConfig), (Sit.SMILES, SmilesSequenceConfig)],
    indirect=["sequence_info_fixture"]
)
def test_sequence_attrs(sequence_info_fixture, expected_config):
    assert sequence_info_fixture.name == expected_config.NAME
    assert sequence_info_fixture.tensor_window_size == expected_config.TENSOR_WINDOW_SIZE
    assert sequence_info_fixture.alphabet == expected_config.ALPHABET
    assert sequence_info_fixture.start_codons == expected_config.START_CODONS
    assert sequence_info_fixture.stop_codons == expected_config.STOP_CODONS
    assert sequence_info_fixture.charset == expected_config.CHARSET


@pytest.mark.parametrize(
    "bio_sequences_fixture, sequence_info_fixture, expected_results",
    [
        (
                (Sit.SMILES, False),
                Sit.SMILES,
                {'valid_count': Tdf.test_real_sequences_limit - Tdf.smiles_test_invalid_sequences_count,
                 'invalid_count': Tdf.smiles_test_invalid_sequences_count}
        ),
    ],
    indirect=["bio_sequences_fixture", "sequence_info_fixture"]
)
def test_filter_invalid_smiles_sequences(sequence_info_fixture, bio_sequences_fixture, expected_results):
    valid_sequences = []
    invalid_sequences = []
    for smiles_sequence in bio_sequences_fixture:
        valid_sequences.append(smiles_sequence) \
            if sequence_info_fixture.is_valid(smiles_sequence) else invalid_sequences.append(smiles_sequence)
    assert len(valid_sequences) == expected_results['valid_count']
    assert len(invalid_sequences) == expected_results['invalid_count']


if __name__ == '__main__':
    pytest.main()
