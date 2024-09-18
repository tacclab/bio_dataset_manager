import pytest

from tests.commons import SequenceInfoTestType as Sit
from tests.commons import TestDatasetFiles as Tdf


@pytest.mark.parametrize(
    "bio_sequences_fixture, sequence_info_fixture, filters, expected_results",
    [

        (  # DNA sequences with valid start, valid len, valid stop, and invalid middle stop
                (Sit.DNA, False),
                Sit.DNA,
                ["has_valid_start", "has_valid_len", "has_valid_stop", "has_invalid_middle_stop"],
                {'valid_count': Tdf.dna_test_valid_sequences_count}
        ),
        (
                (Sit.DNA, False),
                Sit.DNA,
                ["has_valid_start"],
                {'valid_count': Tdf.test_real_sequences_limit - Tdf.dna_test_invalid_start_sequences_count}
        ),
        (
                (Sit.DNA, False),
                Sit.DNA,
                ["has_valid_stop"],
                {'valid_count': Tdf.test_real_sequences_limit - Tdf.dna_test_invalid_stop_sequences_count}
        ),
        (
                (Sit.DNA, False),
                Sit.DNA,
                ["has_invalid_middle_stop"],
                {'valid_count': Tdf.test_real_sequences_limit - Tdf.dna_test_invalid_middle_stop_sequences_count}
        ),
        (
                (Sit.DNA, False),
                Sit.DNA,
                ["has_valid_len"],
                {'valid_count': Tdf.test_real_sequences_limit - Tdf.dna_test_invalid_len_sequences_count}
        ),
        (  # PROTEIN sequences with valid start, valid len, valid stop, and invalid middle stop
                (Sit.PROTEIN, False),
                Sit.PROTEIN,
                ["has_valid_start", "has_valid_len", "has_valid_stop", "has_invalid_middle_stop"],
                {'valid_count': Tdf.protein_test_valid_sequences_count}
        ),
        (
                (Sit.PROTEIN, False),
                Sit.PROTEIN,
                ["has_valid_start"],
                {'valid_count': Tdf.test_real_sequences_limit - Tdf.protein_test_invalid_start_sequences_count}
        ),
        (
                (Sit.PROTEIN, False),
                Sit.PROTEIN,
                ["has_valid_stop"],
                {'valid_count': Tdf.test_real_sequences_limit - Tdf.protein_test_invalid_stop_sequences_count}
        ),
        (
                (Sit.PROTEIN, False),
                Sit.PROTEIN,
                ["has_invalid_middle_stop"],
                {'valid_count': Tdf.test_real_sequences_limit - Tdf.protein_test_invalid_middle_stop_sequences_count}
        ),
        (
                (Sit.PROTEIN, False),
                Sit.PROTEIN,
                ["has_valid_len"],
                {'valid_count': Tdf.test_real_sequences_limit - Tdf.protein_test_invalid_len_sequences_count}
        ),
        (
                (Sit.SMILES, False),
                Sit.SMILES,
                ["has_valid_len"],
                {'valid_count': Tdf.test_real_sequences_limit - Tdf.smiles_test_invalid_len_sequences_count}
        ),
    ],
    indirect=["bio_sequences_fixture", "sequence_info_fixture"]
)
def test_filter_sequences(bio_sequences_utils_fixture, sequence_info_fixture, bio_sequences_fixture, filters,
                          expected_results):
    filtered_sequences = bio_sequences_utils_fixture.filter_sequences(bio_sequences_fixture, filters)
    assert len(filtered_sequences) == expected_results["valid_count"]


@pytest.mark.parametrize(
    "sequence_info_fixture, dna_sequences_fixture, expected_results",
    [
        (Sit.DNA, "ATGCCCTGA", "MP*"),
    ],
    indirect=["sequence_info_fixture"]
)
def test_dna_to_protein(bio_sequences_utils_fixture, sequence_info_fixture, dna_sequences_fixture, expected_results):
    assert bio_sequences_utils_fixture.dna_to_protein(dna_sequences_fixture) == expected_results


@pytest.mark.parametrize(
    "sequence_info_fixture, dna_sequence_fixture",
    [
        (Sit.DNA, "INVALID_SEQUENCE"),
        (Sit.DNA, None),
    ],
    indirect=["sequence_info_fixture"]
)
def test_dna_to_protein_invalid_sequence(bio_sequences_utils_fixture, sequence_info_fixture, dna_sequence_fixture):
    with pytest.raises(ValueError):
        bio_sequences_utils_fixture.dna_to_protein(dna_sequence_fixture)


if __name__ == '__main__':
    pytest.main()
