import numpy as np
import matplotlib.pyplot as plt
from typing import List
from .types import HistoryTraining


class PlotData:

    @staticmethod
    def plot_kfold_summary(results_list: List[HistoryTraining]) -> None:
        """Plots the summary of K-Fold Cross-Validation results.
        Args:
            results_list (list of dicts): A list where each element is a dictionary containing the
                                          results for each fold. Each dictionary contains:
                                          {
                                            "train_loss": [...],
                                            "val_loss": [...],
                                            "train_acc": [...],
                                            "val_acc": [...]
                                          }
        """
        # Initialize lists to hold the metrics for each fold
        train_losses = []
        val_losses = []
        train_accuracies = []
        val_accuracies = []

        # Collect results from each fold
        for results in results_list:
            train_losses.append(results["train_loss"])
            val_losses.append(results["val_loss"])
            train_accuracies.append(results["train_acc"])
            val_accuracies.append(results["val_acc"])

        # Convert lists to numpy arrays for easier manipulation
        train_losses = np.array(train_losses)
        val_losses = np.array(val_losses)
        train_accuracies = np.array(train_accuracies)
        val_accuracies = np.array(val_accuracies)

        # Calculate mean and standard deviation across folds for each metric
        mean_train_loss = np.mean(train_losses, axis=0)
        std_train_loss = np.std(train_losses, axis=0)
        mean_val_loss = np.mean(val_losses, axis=0)
        std_val_loss = np.std(val_losses, axis=0)

        mean_train_acc = np.mean(train_accuracies, axis=0)
        std_train_acc = np.std(train_accuracies, axis=0)
        mean_val_acc = np.mean(val_accuracies, axis=0)
        std_val_acc = np.std(val_accuracies, axis=0)

        epochs = range(len(mean_train_loss))

        # Plot the mean and standard deviation for Loss
        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        plt.plot(epochs, mean_train_loss, label="Mean Train Loss")
        plt.fill_between(epochs, mean_train_loss - std_train_loss,
                         mean_train_loss + std_train_loss, alpha=0.3)
        plt.plot(epochs, mean_val_loss, label="Mean Validation Loss")
        plt.fill_between(epochs, mean_val_loss - std_val_loss,
                         mean_val_loss + std_val_loss, alpha=0.3)
        plt.title("Loss Summary")
        plt.xlabel("Epochs")
        plt.ylabel("Loss")
        plt.legend()

        # Plot the mean and standard deviation for Accuracy
        plt.subplot(1, 2, 2)
        plt.plot(epochs, mean_train_acc, label="Mean Train Accuracy")
        plt.fill_between(epochs, mean_train_acc - std_train_acc,
                         mean_train_acc + std_train_acc, alpha=0.3)
        plt.plot(epochs, mean_val_acc, label="Mean Validation Accuracy")
        plt.fill_between(epochs, mean_val_acc - std_val_acc,
                         mean_val_acc + std_val_acc, alpha=0.3)
        plt.title("Accuracy Summary")
        plt.xlabel("Epochs")
        plt.ylabel("Accuracy")
        plt.legend()

        plt.suptitle("K-Fold Cross-Validation Summary")
        plt.show()

    @staticmethod
    def plot_curves_summary(results: HistoryTraining):
        """Plots training curves of a results dictionary.

        Args:
            results (dict): dictionary containing list of values, e.g.
                {"train_loss": [...],
                 "train_acc": [...],
                 "val_loss": [...],
                 "val_acc": [...]}
        """
        train_loss = results["train_loss"]
        val_loss = results["val_loss"]

        accuracy = results["train_acc"]
        val_accuracy = results["val_acc"]

        epochs = range(len(results["train_loss"]))

        plt.figure(figsize=(12, 5))

        # Plot loss
        plt.subplot(1, 2, 1)
        plt.plot(epochs, train_loss, label="train_loss")
        plt.plot(epochs, val_loss, label="val_loss")
        plt.title("Loss")
        plt.xlabel("Epochs")
        plt.legend()

        # Plot accuracy
        plt.subplot(1, 2, 2)
        plt.plot(epochs, accuracy, label="train_accuracy")
        plt.plot(epochs, val_accuracy, label="val_accuracy")
        plt.title("Accuracy")
        plt.xlabel("Epochs")
        plt.legend()
