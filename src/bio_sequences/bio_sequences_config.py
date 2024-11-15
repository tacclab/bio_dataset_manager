from dataclasses import dataclass


@dataclass
class BioSequenceConfig:
    NAME: str = "BIO-SEQUENCE"
    START_CODONS: list = "C",
    STOP_CODONS: list = "T"
    CHARSET: list = "C", "A", "R", "S", "E", "T"
    ALPHABET: str = ''.join(CHARSET)
    TENSOR_WINDOW_SIZE: int = 4


@dataclass
class ProteinSequenceConfig:
    NAME = "PROTEIN"
    CHARSET = [
        "A",  # Alanine
        "R",  # Arginine
        "N",  # Asparagine
        "D",  # Aspartic acid
        "C",  # Cysteine
        "E",  # Glutamic acid
        "Q",  # Glutamine
        "G",  # Glycine
        "H",  # Histidine
        "I",  # Isoleucine
        "L",  # Leucine
        "K",  # Lysine
        "M",  # Methionine
        "F",  # Phenylalanine
        "P",  # Proline
        "S",  # Serine
        "T",  # Threonine
        "W",  # Tryptophan
        "Y",  # Tyrosine
        "V",  # Valine
        "*",  # Stop codon (termination of the protein sequence)
    ]
    ALPHABET = ''.join(CHARSET)
    STOP_CODONS = ["*"]
    START_CODONS = ["M"]
    TENSOR_WINDOW_SIZE = 1


@dataclass
class DnaSequenceConfig:
    NAME = "DNA"
    CHARSET = [
        "A",  # Adenine
        "C",  # Cytosine
        "G",  # Guanine
        "T"  # Thymine
    ]
    ALPHABET = ''.join(CHARSET)
    START_CODONS = ["ATG"]
    STOP_CODONS = ["TAA", "TAG", "TGA"]
    TENSOR_WINDOW_SIZE = 3


@dataclass
class SmilesSequenceConfig:
    NAME = "SMILES"
    CHARSET = [
        'B', 'C', 'N', 'O', 'P', 'S', 'F', 'Cl', 'Br', 'I',  # Organic atoms
        '[', ']',  # Brackets for special atoms
        '=', '#', '-', ':',  # Bonds (double, triple, single, aromatic)
        '1', '2', '3', '4', '5', '6', '7', '8', '9',  # Ring closures
        '(', ')',  # Branches
        'c', 'n', 'o', 'p', 's',  # Aromatic atoms (lowercase)
        '@', '@@',  # Chirality symbols
        '+', '-',  # Charges
        'H', 'h',  # Hydrogen count indicators
        '.',  # Delimiter
        'l',  # Linkers
        'K',  # Kekulization
    ]
    ALPHABET = ''.join(CHARSET)
    START_CODONS = []
    STOP_CODONS = []
    TENSOR_WINDOW_SIZE = 1
