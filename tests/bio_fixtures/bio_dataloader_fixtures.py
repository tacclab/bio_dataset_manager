import torch.cuda
from pytest import fixture

from bio_dataset_manager.bio_dataloader import BioDataloader
from bio_dataset_manager.bio_dataset import BioDataset


@fixture
def dataloader_params():
    return {
        'use_gpu': True if torch.cuda.is_available() else False,
        'batch_size': 3,
        'shuffle': True,
        'collate_fn': BioDataset.collate_fn,
        'split_ratio': 0.2,
    }


@fixture
def bio_dataloader_fixture(bio_dataset_fixture, dataloader_params):
    return BioDataloader(dataset=bio_dataset_fixture, **dataloader_params)
