from abc import ABC, abstractmethod

from src.bio_sequences.bio_sequences_config import BioSequenceConfig


class BioSequence(ABC):
    """
    Abstract base class for bio sequences. Both ProteinSequence and DnaSequence
    will inherit from this class to share common properties and methods.

    Args:
        config (BioSequenceConfig): The configuration for the bio sequence.

    Attributes:
        _name (str): The name of the bio sequence.
        _alphabet (str): The alphabet of the bio sequence.
        _start_codons (list): The start codons of the bio sequence.
        _stop_codons (list): The stop codons of the bio sequence.
        _charset (list): The charset of the bio sequence.
        _tensor_window_size (int): The tensor window size of the bio sequence.

    """

    def __init__(self, config: BioSequenceConfig):
        self._config = config
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

    @property
    def charset(self):
        return self._charset

    @charset.setter
    def charset(self, value):
        self._charset = value

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

    @abstractmethod
    def has_valid_start(self, sequence: str) -> bool:
        pass

    @abstractmethod
    def has_valid_stop(self, sequence: str) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def has_valid_len(sequence: str, valid_range: range or None = None) -> bool:
        pass

    @abstractmethod
    def has_invalid_middle_stop(self, sequence: str) -> bool:
        pass
