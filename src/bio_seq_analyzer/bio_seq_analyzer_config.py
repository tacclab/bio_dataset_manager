import enum
from dataclasses import dataclass


class BioSeqAnalyzerMeasures(enum.Enum):
    """
    'sequence_similarity_score': self.sequence_similarity_score,
    'sequence_gc_content': self.sequence_gc_content,
    'chargaff_pf': self.chargaff_pf,
    'chargaff_ct': self.chargaff_ct,
    'valid_syntax': self.valid_syntax,
    """


@dataclass
class BioSeqAnalyzerConfig:
    pass


@dataclass
class BioSeqAnalyzerDnaConfig(BioSeqAnalyzerConfig):
    pass


@dataclass
class BioSeqAnalyzerProteinConfig(BioSeqAnalyzerConfig):
    pass


@dataclass
class BioSeqAnalyzerSmilesConfig(BioSeqAnalyzerConfig):
    pass

