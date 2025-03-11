import time

import torch
from tqdm import tqdm

from bio_dataset_manager.bio_dataloader import BioDataloader
from bio_dataset_manager.bio_dataset import BioDataset
from bio_sequences.dna_sequence import DnaSequence
from bio_sequences.protein_sequence import ProteinSequence
from bio_sequences.smiles_sequence import SmilesSequence


def demo(sequence_info: DnaSequence or ProteinSequence or SmilesSequence, dataset_folder: str = None):
    # example usage for DnaSequences loaded from a file
    # if you want to pass a list of sequences, set this to sequences=[sequence1, sequence2, ...] and dataset_folder=None
    dataset = BioDataset(
        dataset_folder=dataset_folder,
        sequences_limit=10,
        randomize_choice=True,
        pad_same_len=False,
        window_size=1,
        sequence_info=sequence_info,
        sequences=None,
    )

    # example usage for DnaSequences loaded from a list
    dataloader = BioDataloader(
        dataset=dataset,
        batch_size=5,
        shuffle=True,
        collate_fn=dataset.collate_fn,
        split_ratio=0.5,
        use_gpu=True if torch.cuda.is_available() else False
    )
    # training loop example
    epochs = 5
    for epoch in range(epochs):
        with tqdm(total=len(dataloader.training_dataloader), desc=f"Epoch {epoch + 1}/{epochs}", unit="batch") as pbar:
            for batch in dataloader.training_dataloader:
                y_real, lengths = dataloader.process_batch(batch)
                time.sleep(0.1)
                pbar.update(1)
                pbar.set_postfix(
                    loss_gen=f"0.0",
                    loss_dis=f"0.0"
                )
        pbar.refresh()


if __name__ == "__main__":
    print("Usage example: DNA")
    demo(DnaSequence(), "../tests/bio_test_samples/dna/")
    print("Usage example: PROTEIN")
    demo(ProteinSequence(), "../tests/bio_test_samples/protein/")
    print("Usage example: SMILES")
    demo(SmilesSequence(), "../tests/bio_test_samples/smiles/")
