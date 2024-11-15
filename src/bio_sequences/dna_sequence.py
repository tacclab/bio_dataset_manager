from src.bio_sequences.bio_sequence import BioSequence
from src.bio_sequences.bio_sequences_config import DnaSequenceConfig


class DnaSequence(BioSequence):
    def __init__(self):
        super().__init__(DnaSequenceConfig())

    def has_valid_start(self, sequence: str) -> bool:
        return sequence[:3] in self.start_codons

    def has_valid_stop(self, sequence: str) -> bool:
        return sequence[-3:] in self.stop_codons

    @staticmethod
    def has_valid_len(sequence: str, valid_range: range or None = None) -> bool:
        sequence_length = len(sequence)
        if valid_range is not None and sequence_length not in valid_range:
            return False
        return sequence_length % 3 == 0

    def has_invalid_middle_stop(self, sequence: str) -> bool:
        sequence_to_check = sequence[3:-3]
        for i in range(0, len(sequence_to_check), 3):
            codon = sequence[i: i + 3]
            if codon in self.stop_codons:
                return False
        return True
