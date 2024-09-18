from src.bio_sequences.bio_sequences_config import DnaSequenceConfig


class DnaSequence:

    def __init__(self):
        self._config = DnaSequenceConfig()
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
    def charset(self) -> list:
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
