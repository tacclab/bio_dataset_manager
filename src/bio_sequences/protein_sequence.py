from src.bio_sequences.bio_sequence import BioSequence
from src.bio_sequences.bio_sequences_config import ProteinSequenceConfig


class ProteinSequence(BioSequence):
    def __init__(self):
        super().__init__(ProteinSequenceConfig())

    def has_valid_start(self, sequence: str) -> bool:
        return sequence[:1] in self.start_codons

    def has_valid_stop(self, sequence: str) -> bool:
        return sequence[-1:] in self.stop_codons

    @staticmethod
    def has_valid_len(sequence: str, valid_range: range or None = None) -> bool:
        sequence_length = len(sequence)
        if valid_range is not None and sequence_length not in valid_range:
            return False
        return True

    def has_invalid_middle_stop(self, sequence: str) -> bool:
        return all([stop_codon not in sequence[1:-1] for stop_codon in self.stop_codons])
