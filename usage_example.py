import time

from tqdm import tqdm

from bio_dataset_manager import BioDataset, BioDataloader
from bio_sequences import DnaSequence, ProteinSequence, SmilesSequence


def demo(sequence_info: DnaSequence or ProteinSequence or SmilesSequence, dataset_folder: str = None):
    # Example usage for DnaSequences loaded from a file
    # If you want to pass a list of sequences, set this to sequences=[sequence1, sequence2, ...] and dataset_folder=None
    dataset = BioDataset(
        dataset_folder=dataset_folder,
        sequences_limit=10,
        randomize_choice=True,
        pad_same_len=False,
        window_size=1,
        sequence_info=sequence_info,
        sequences=None,
    )
    # print(dataset.sequences)

    # Example usage for DnaSequences loaded from a list
    dataloader = BioDataloader(
        dataset=dataset,
        batch_size=5,
        shuffle=True,
        collate_fn=dataset.collate_fn,
        split_ratio=0.5,
        use_gpu=True
    )
    # print(dataloader.training_dataloader)
    # print(dataloader.validation_dataloader)

    # Training loop example
    epochs = 5
    for epoch in range(epochs):
        with tqdm(total=len(dataloader.training_dataloader), desc=f"Epoch {epoch + 1}/{epochs}", unit="batch") as pbar:
            for batch in dataloader.training_dataloader:
                y_real, lengths = dataloader.process_batch(batch)
                print(f"Real sequences: {len(lengths)}, Real sequences Lengths: {lengths}")
                time.sleep(0.1)
                pbar.update(1)
                pbar.set_postfix(
                    loss_gen=f"0.0",
                    loss_dis=f"0.0"
                )
        pbar.refresh()


if __name__ == "__main__":
    print("\nUsage example: DNA\n")
    demo(DnaSequence(), "tests/bio_test_samples/dna/")
    print("\nUsage example: PROTEIN\n")
    demo(ProteinSequence(), "tests/bio_test_samples/protein/")
    print("\nUsage example: SMILES\n")
    demo(SmilesSequence(), "tests/bio_test_samples/smiles/")
