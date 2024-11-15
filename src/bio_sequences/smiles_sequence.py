from rdkit import Chem

from src.bio_sequences.bio_sequence import BioSequence
from src.bio_sequences.bio_sequences_config import SmilesSequenceConfig


class SmilesSequence(BioSequence):
    """
    SMILES sequence class for validating and handling SMILES string representations of molecules.
    """

    def __init__(self):
        super().__init__(SmilesSequenceConfig())

    def has_valid_start(self, sequence: str) -> bool:
        """
        Checks if the SMILES sequence starts with a valid start codon (not applicable for SMILES).
        """
        return True

    def has_valid_stop(self, sequence: str) -> bool:
        """
        Checks if the SMILES sequence ends with a valid stop codon (not applicable for SMILES).
        """
        return True

    @staticmethod
    def has_valid_len(sequence: str, valid_range: range or None = None) -> bool:
        """
        Validates the length of the SMILES sequence.
        """
        return True

    def has_invalid_middle_stop(self, sequence: str) -> bool:
        """
        Check if a stop codon appears in the middle of the SMILES sequence.
        """
        # This can be SMILES-specific, but for simplicity we return True.
        return False

    @staticmethod
    def is_valid(sequence: str) -> bool:
        """
        Validates if the SMILES sequence is a valid SMILES representation.
        """
        try:
            molecule = Chem.MolFromSmiles(sequence)
        except ValueError as _:
            molecule = None
        return True if molecule else False
