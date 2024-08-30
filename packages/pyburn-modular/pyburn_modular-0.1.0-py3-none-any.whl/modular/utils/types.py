from typing import TypedDict, List


class HistoryTraining(TypedDict):
    train_loss: List[float]
    train_acc: List[float]
    val_loss: List[float]
    val_acc: List[float]
