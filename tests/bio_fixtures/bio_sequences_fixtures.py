from Bio import SeqIO
from pytest import fixture

from bio_sequences.bio_sequences_utils import BioSequencesUtils
from bio_sequences.dna_sequence import DnaSequence
from bio_sequences.protein_sequence import ProteinSequence
from bio_sequences.smiles_sequence import SmilesSequence
from tests.commons import SequenceInfoTestType as Sit
from tests.commons import TestDatasetFiles as Tdf


@fixture
def dna_fixture():
    return DnaSequence()


@fixture
def protein_fixture():
    return ProteinSequence()


@fixture
def smiles_fixture():
    return SmilesSequence()


@fixture
def sequence_info_fixture(request, dna_fixture, protein_fixture, smiles_fixture):
    if request.param == Sit.DNA:
        return dna_fixture
    if request.param == Sit.PROTEIN:
        return protein_fixture
    if request.param == Sit.SMILES:
        return smiles_fixture
    raise ValueError(f"Invalid sequence type: {request.param}")


@fixture
def bio_sequences_utils_fixture(sequence_info_fixture):
    return BioSequencesUtils(sequence_info=sequence_info_fixture, valid_range=range(300, 2000))


@fixture
def dna_sequences_fixture():
    with open(Tdf.dna_test_dataset_file, "r") as file:
        data = [str(record.seq) for record in SeqIO.parse(file, "fasta")]
        if Tdf.test_real_sequences_limit < len(data):
            raise ValueError(f"Invalid samples number limit: {Tdf.test_real_sequences_limit}")
    return data[:Tdf.test_real_sequences_limit]


@fixture
def protein_sequences_fixture():
    with open(Tdf.protein_test_dataset_file, "r") as file:
        data = [str(record.seq) for record in SeqIO.parse(file, "fasta")]
        if Tdf.test_real_sequences_limit < len(data):
            raise ValueError(f"Invalid samples number limit: {Tdf.test_real_sequences_limit}")
    return data[:Tdf.test_real_sequences_limit]


@fixture
def smiles_sequences_fixture():
    with open(Tdf.smiles_test_dataset_file, "r") as file:
        data = [str(record.seq) for record in SeqIO.parse(file, "fasta")]
        if Tdf.test_real_sequences_limit < len(data):
            raise ValueError(f"Invalid samples number limit: {Tdf.test_real_sequences_limit}")
    return data[:Tdf.test_real_sequences_limit]


@fixture
def bio_sequences_fixture(request, dna_sequences_fixture, protein_sequences_fixture, smiles_sequences_fixture):
    sequence_type, only_valid = request.param
    if sequence_type not in [Sit.DNA, Sit.PROTEIN, Sit.SMILES]:
        raise ValueError(f"Invalid sequence type: {sequence_type}")

    sequences = []
    only_valid_limit = None

    if sequence_type == Sit.DNA:
        sequences = dna_sequences_fixture
        only_valid_limit = Tdf.dna_test_valid_sequences_count
    if sequence_type == Sit.PROTEIN:
        sequences = protein_sequences_fixture
        only_valid_limit = Tdf.protein_test_valid_sequences_count
    if sequence_type == Sit.SMILES:
        sequences = smiles_sequences_fixture
        only_valid_limit = Tdf.smiles_test_valid_sequences_count

    return sequences[:only_valid_limit] if only_valid else sequences
