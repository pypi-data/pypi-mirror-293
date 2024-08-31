
import torch
from torch.utils.data import DataLoader, Dataset
from modular.utils.functional import F
from modular.utils.default_args import NUM_WORKERS, BATCH_SIZE


def create_dataloader(dataset: Dataset,
                      *,
                      batch_size: int = BATCH_SIZE,
                      shuffle: bool = False,
                      number_workers: int = NUM_WORKERS,
                      pin_memory: bool = False,
                      device: torch.device = torch.device("cpu")):

    dataloader = DataLoader(dataset,
                            batch_size=batch_size,
                            shuffle=shuffle,
                            num_workers=number_workers,
                            pin_memory=pin_memory or F.is_cuda_device(device))

    return dataloader
