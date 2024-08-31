import os
import sys
import time
import torch
import numpy as np
from typing import Any, Generator


def progress_bar(iter, *, prefix="", size=40, out=sys.stdout) -> Generator[Any, Any, None]:
    count = len(iter)
    start = time.time()

    def show(j: int) -> None:
        x = int(size*j/count)
        remaining = ((time.time() - start) / j) * (count - j)
        mins, sec = divmod(remaining, 60)
        time_str = f"{int(mins):02}:{sec:05.2f}"

        print(f"{prefix}[{u'█'*x}{('.'*(size-x))}] {j}/{count} Est wait {time_str}",
              end='\r', file=out, flush=True)

    for i, item in enumerate(iter):
        yield item
        show(i+1)
    print("\n", flush=True, file=out)


def walk_through_dir(dir_path):
    """
    Walks through dir_path returning its contents.
    Args:
    dir_path (str): target directory

    Returns:
    A print out of:
      number of subdirectories in dir_path
      number of images (files) in each subdirectory
      name of each subdirectory
    """
    for dirpath, dirnames, filenames in os.walk(dir_path):
        print(
            f"There are {len(dirnames)} directories and {len(filenames)} file in '{dirpath}'.")


class F:
    @staticmethod
    def is_cuda_device(device: torch.device):
        return device.type == "cuda"

    @staticmethod
    def seed_everything(seed_value):
        np.random.seed(seed_value)
        torch.manual_seed(seed_value)
        if torch.cuda.is_available():
            torch.cuda.manual_seed(seed_value)
            torch.cuda.manual_seed_all(seed_value)
        if torch.backends.mps.is_available():
            torch.mps.manual_seed(seed_value)

    @staticmethod
    def set_device() -> torch.device:
        device = torch.device("cpu")
        if torch.cuda.is_available():
            device = torch.device("cuda")
        elif torch.backends.mps.is_available():
            device = torch.device("mps")
        return device

    @staticmethod
    def save_state_model(model: torch.nn.Module, save_path: str | os.PathLike) -> None:
        print(f"Saving model state to: {save_path}")
        torch.save(obj=model.state_dict(), f=save_path)

    @staticmethod
    def save_entire_model(model: torch.nn.Module, save_path:  str | os.PathLike) -> None:
        print(f"Saving model to: {save_path}")
        torch.save(model, f=save_path)

    @staticmethod
    def accuracy_fn(y_pred: torch.Tensor, y_true: torch.Tensor) -> float:
        """Calculates accuracy between truth labels and predictions.

        Args:
            y_true (torch.Tensor): Truth labels for predictions.
            y_pred (torch.Tensor): Predictions to be compared to predictions.

        Returns:
            [torch.float]: Accuracy value between y_true and y_pred, e.g. 78.45
        """
        correct = torch.eq(y_pred, y_true).sum().item()
        acc = correct / len(y_pred)
        return acc
