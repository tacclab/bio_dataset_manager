from abc import ABC, abstractmethod
from typing import List

from src.bio_sequences.bio_sequences_utils import BioSequencesUtils
from src.bio_sequences.dna_sequence import DnaSequence
from src.bio_sequences.protein_sequence import ProteinSequence
from src.bio_sequences.smiles_sequence import SmilesSequence


class BioSeqAnalyzer(ABC):
    def __init__(
            self,
            real_sequences: list,
            sequence_info: ProteinSequence or DnaSequence or SmilesSequence,
            utils: BioSequencesUtils
    ):
        self.real_sequences = real_sequences
        self.sequence_info = sequence_info
        self.utils = utils
        self.measures = self.list_measures()

    def list_measures(self) -> List[str]:
        # Automatically find methods ending with '_measure'
        return [method for method in dir(self) if method.endswith('_measure')]

    @abstractmethod
    def analyze(self) -> None:
        raise NotImplementedError


class DnaSeqAnalyzer(BioSeqAnalyzer):
    def analyze(self) -> None:
        print("Analyzing DNA sequences...")
        # Perform DNA-specific analysis
        # Example:
        for sequence in self.real_sequences:
            print(f"Processed DNA: {sequence}")


# Concrete analyzer for protein sequences
class ProteinSeqAnalyzer(BioSeqAnalyzer):
    def analyze(self) -> None:
        print("Analyzing protein sequences...")
        # Perform protein-specific analysis
        # Example:
        for sequence in self.real_sequences:
            print(f"Processed Protein: {sequence}")


# Concrete analyzer for SMILES sequences
class SmilesSeqAnalyzer(BioSeqAnalyzer):
    def analyze(self) -> None:
        print("Analyzing SMILES sequences...")
        # Perform SMILES-specific analysis
        # Example:
        for sequence in self.real_sequences:
            print(f"Processed SMILES: {sequence}")
