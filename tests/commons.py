import os
from dataclasses import dataclass
from enum import Enum

base_dir = os.path.dirname(os.path.abspath(__file__))  # Directory containing common.py


@dataclass
class TestDatasetFiles:
    test_real_sequences_limit = 10

    # DNA test dataset files: counts depends on sequences in the test file
    dna_test_dataset_file = os.path.join(base_dir, "./bio_test_samples/dna/dna_test_sequences.fna")
    dna_test_valid_sequences_count = 6
    dna_test_invalid_stop_sequences_count = 1
    dna_test_invalid_middle_stop_sequences_count = 1
    dna_test_invalid_len_sequences_count = 1
    dna_test_invalid_start_sequences_count = 1

    # PROTEIN test dataset files: counts depends on sequences in the test file
    protein_test_dataset_file = os.path.join(base_dir, "./bio_test_samples/protein/protein_test_sequences.fna")
    protein_test_valid_sequences_count = 6
    protein_test_invalid_stop_sequences_count = 1
    protein_test_invalid_middle_stop_sequences_count = 1
    protein_test_invalid_len_sequences_count = 1
    protein_test_invalid_start_sequences_count = 1

    # SMILES test dataset files: counts depends on sequences in the test file
    smiles_test_dataset_file = os.path.join(base_dir, "./bio_test_samples/smiles/smiles_test_sequences.fna")
    smiles_test_valid_sequences_count = 6
    smiles_test_invalid_sequences_count = 3
    smiles_test_invalid_stop_sequences_count = 0
    smiles_test_invalid_middle_stop_sequences_count = 0
    smiles_test_invalid_len_sequences_count = 0
    smiles_test_invalid_start_sequences_count = 0


class PaddingLengthTestOptions(Enum):
    SAME = "same_len"
    LONGER = "longer"


class SequenceInfoTestType(Enum):
    DNA = "dna"
    PROTEIN = "protein"
    SMILES = "smiles"
