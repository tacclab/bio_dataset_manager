from Bio.Seq import Seq

from src.bio_sequences.dna_sequence import DnaSequence
from src.bio_sequences.protein_sequence import ProteinSequence


class BioSequencesUtils:
    def __init__(self, sequence_info: ProteinSequence or DnaSequence, valid_range: list = range(3, 2830)):
        self.sequence_info = sequence_info

        # Initialize the sequence filters
        self.sequence_filters = {
            "has_valid_start": self.sequence_info.has_valid_start,
            "has_valid_stop": self.sequence_info.has_valid_stop,
            "has_invalid_middle_stop": self.sequence_info.has_invalid_middle_stop,
            "has_valid_len": lambda seq: self.sequence_info.has_valid_len(seq, valid_range),
        }

    def filter_sequences(self, sequences: list, filters: list) -> list:
        """
        Filter the sequences based on the filters
        :param sequences:
        :param filters:
        :return:
        """
        filtered_sequences = []

        for seq_filter in filters:
            if seq_filter not in self.sequence_filters.keys():
                raise ValueError(f"Invalid filter: {seq_filter}")

        for sequence in sequences:
            if all([self.sequence_filters[seq_filter](sequence) for seq_filter in filters]):
                filtered_sequences.append(sequence)

        return filtered_sequences

    @staticmethod
    def dna_to_protein(sequence: str) -> str:
        """
        Translate the DNA sequence to a protein sequence
        :param sequence: str of a sequence in fasta format
        :return: str containing the protein sequence in fasta format
        """
        if sequence is None:
            raise ValueError("A DNA sequence must be provided")
        try:
            dna_seq = Seq(sequence)
            protein_sequence = dna_seq.translate()
        except Exception as _:
            raise ValueError("Invalid DNA sequence provided")
        return protein_sequence
