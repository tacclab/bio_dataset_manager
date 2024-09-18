from rdkit import Chem

from src.bio_sequences.bio_sequences_config import SmilesSequenceConfig


class SmilesSequence:
    def __init__(self):
        self._config = SmilesSequenceConfig()
        self._name = self._config.NAME
        self._alphabet = self._config.ALPHABET
        self._start_codons = self._config.START_CODONS
        self._stop_codons = self._config.STOP_CODONS
        self._charset = self._config.CHARSET
        self._tensor_window_size = self._config.TENSOR_WINDOW_SIZE

    @property
    def tensor_window_size(self):
        return self._tensor_window_size

    @tensor_window_size.setter
    def tensor_window_size(self, value: int):
        self._tensor_window_size = value

    @tensor_window_size.getter
    def tensor_window_size(self):
        return self._tensor_window_size

    @property
    def charset(self):
        return self._charset

    @charset.setter
    def charset(self, value):
        self._charset = value

    @charset.getter
    def charset(self):
        return self._charset

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def alphabet(self):
        return self._alphabet

    @alphabet.setter
    def alphabet(self, value):
        self._alphabet = value

    @property
    def start_codons(self):
        return self._start_codons

    @start_codons.setter
    def start_codons(self, value):
        self._start_codons = value

    @property
    def stop_codons(self):
        return self._stop_codons

    @stop_codons.setter
    def stop_codons(self, value):
        self._stop_codons = value

    @staticmethod
    def has_valid_start(sequence: str) -> bool:
        return True

    @staticmethod
    def has_valid_stop(sequence: str) -> bool:
        return True

    @staticmethod
    def has_valid_len(sequence: str, valid_range: range or None = None) -> bool:
        return True

    @staticmethod
    def has_invalid_middle_stop(sequence: str) -> bool:
        return True

    @staticmethod
    def is_valid(sequence: str) -> bool:
        try:
            molecule = Chem.MolFromSmiles(sequence)
        except ValueError as _:
            molecule = None
        return True if molecule else False
