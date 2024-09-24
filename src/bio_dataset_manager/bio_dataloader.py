import torch
from src.bio_dataset_manager.bio_dataset import BioDataset
from torch.nn.utils.rnn import pad_packed_sequence
from torch.utils.data import DataLoader
from torch.utils.data import random_split


class BioDataloader:
    def __init__(self,
                 dataset: BioDataset,
                 use_gpu: bool,
                 batch_size: int,
                 shuffle: bool,
                 collate_fn: BioDataset.collate_fn or None,
                 split_ratio: float
                 ):
        self.training_dataloader = None
        self.validation_dataloader = None
        self.dataset = dataset
        self.shuffle = shuffle
        self.collate_fn = collate_fn
        self.batch_size = batch_size
        self.split_ratio = split_ratio
        self.use_gpu = use_gpu

        self.training_dataset = None
        self.validation_dataset = None

        self.init_dataloader(self.split_ratio)

    def init_dataloader(self, split_ratio: float) -> None:
        """
        Initialize the dataloader
        :param split_ratio:
        :return:
        """
        training_dataset, validation_dataset = self.split_dataset(split_ratio)

        self.training_dataloader = self.create_dataloader(training_dataset, shuffle=self.shuffle)
        self.validation_dataloader = self.create_dataloader(validation_dataset, shuffle=False)

        if self.use_gpu:
            self.training_dataloader = self.move_dataloader_to_gpu(self.training_dataloader)
            self.validation_dataloader = self.move_dataloader_to_gpu(self.validation_dataloader)

    def create_dataloader(self, dataset: torch.utils.data.Dataset, shuffle: bool) -> DataLoader:
        """
        Create a dataloader for the dataset
        :param dataset:
        :param shuffle:
        :return: dataloader
        """
        return DataLoader(
            dataset,
            batch_size=self.batch_size,
            shuffle=shuffle,
            collate_fn=self.collate_fn,
            drop_last=True,
        )

    @staticmethod
    def move_dataloader_to_gpu(dataloader: DataLoader) -> DataLoader:
        """
        Move the dataloader to GPU
        :param dataloader:
        :return: dataloader_gpu
        """
        dataloader_gpu = [(inputs.cuda(), labels) for inputs, labels in dataloader]
        return dataloader_gpu

    def split_dataset(self, split_ratio: float) -> (torch.utils.data.Dataset, torch.utils.data.Dataset):
        """
        Split the dataset into training and validation sets
        :param split_ratio: float
        :return: training_dataset, validation_dataset
        """
        dataset_size = len(self.dataset)
        validation_size = int(dataset_size * split_ratio)
        training_size = dataset_size - validation_size

        if self.batch_size > training_size:
            raise ValueError(
                f"The batch size {self.batch_size} is larger than the number of training samples {training_size}.")

        # Split the dataset into training and validation sets
        training_dataset, validation_dataset = random_split(self.dataset, [training_size, validation_size])

        self.training_dataset = training_dataset
        self.validation_dataset = validation_dataset
        return training_dataset, validation_dataset

    def process_batch(self, batch: tuple, batch_first: bool = True) -> (torch.Tensor, list):
        packed_inputs, _ = batch
        y_real, lengths = pad_packed_sequence(packed_inputs, batch_first=True)
        return y_real, lengths
