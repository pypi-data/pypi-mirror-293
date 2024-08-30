
import torch
import torch.utils
import torch.utils.data
from typing import Tuple
from timeit import default_timer as timer
from .utils.functional import F
from .utils import HistoryTraining, progress_bar
from .utils.default_args import NUM_EPOCHS


class Engine:

    def __init__(self,
                 model: torch.nn.Module,
                 train_dataloader: torch.utils.data.DataLoader,
                 val_dataloader: torch.utils.data.DataLoader,
                 *,
                 loss_fn: torch.nn.Module,
                 optimizer: torch.optim.Optimizer,
                 scheduler: torch.optim.Optimizer,
                 epochs: int = NUM_EPOCHS,
                 device: torch.device = torch.device("cpu"),
                 multi_label: bool = True) -> None:

        self.model: torch.nn.Module = model
        self.train_dataloader: torch.utils.data.DataLoader = train_dataloader
        self.val_dataloader: torch.utils.data.DataLoader = val_dataloader
        self.loss_fn: torch.nn.Module = loss_fn
        self.optimizer: torch.optim.Optimizer = optimizer
        self.scheduler: torch.optim.Optimizer = scheduler
        self.epochs: int = epochs
        self.device: torch.device = device
        self.multi_label: bool = multi_label
        self.history: HistoryTraining = {
            "train_loss": [],
            "train_acc": [],
            "val_loss": [],
            "val_acc": []
        }

    def train_step(self) -> Tuple[float, float]:
        running_loss = 0.0
        correct = 0
        total = len(self.train_dataloader)
        self.model.train()
        for batch in self.train_dataloader:
            X = batch[0].to(self.device)
            y_train = batch[1].to(self.device)

            # 1. Forward pass
            y_logit = self.model(
                X) if self.multi_label else self.model(X).squeeze()

            # 2. Calculate the loss
            loss = self.loss_fn(y_logit, y_train)
            running_loss += loss.item()

            # 3. Zero gradients
            self.optimizer.zero_grad()

            # 4. Perform back propagation on the loss
            loss.backward()

            # 5. Update the optimizer (gradient descent)
            self.optimizer.step()

            # calculate summary
            y_pred = self.__predict_from_logit(y_logit)
            correct += F.accuracy_fn(y_pred, y_train)

        train_loss = running_loss / total
        accuracy = correct / total
        return train_loss, accuracy

    def eval_step(self) -> Tuple[float, float]:
        running_loss = 0.0
        correct = 0
        total = len(self.val_dataloader)
        self.model.eval()
        with torch.inference_mode():
            for batch in self.val_dataloader:
                X = batch[0].to(self.device)
                y_train = batch[1].to(self.device)
                y_logit = self.model(
                    X) if self.multi_label else self.model(X).squeeze()
                loss = self.loss_fn(y_logit, y_train)
                running_loss += loss.item()
                y_pred = self.__predict_from_logit(y_logit)
                correct += F.accuracy_fn(y_pred, y_train)

        val_loss = running_loss / total
        accuracy = correct / total
        return val_loss, accuracy

    def __predict_from_logit(self, y_logit: torch.Tensor) -> torch.Tensor:
        return torch.argmax(torch.softmax(y_logit, dim=1), dim=1) if self.multi_label else torch.round(torch.sigmoid(y_logit))

    def train(self) -> HistoryTraining:
        start_time = timer()
        for epoch in progress_bar(range(self.epochs)):
            print(f"Starting training for Epoch: {epoch+1} / {self.epochs}")
            train_loss, train_acc = self.train_step()
            val_loss, val_acc = self.eval_step()
            self.history["train_loss"].append(train_loss)
            self.history["train_acc"].append(train_acc)
            self.history["val_loss"].append(val_loss)
            self.history["val_acc"].append(val_acc)
            print(
                f"Train_Loss: {train_loss:.5f} | Train_Acc: {train_acc:.2f} | Val_Loss: {val_loss:.5f} | Val_Acc: {val_acc:.2f}")
            self.scheduler.step(val_acc)
            print("=================================================================")
        end_time = timer()
        print(
            f"[INFO] Train time on {self.device}: {end_time - start_time:.3f} seconds")
        return self.history
