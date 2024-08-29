import numpy as np
import torch.nn as nn
import torch
import torch.nn.functional as F
import pandas as pd
from torch.utils.data import DataLoader
from typing import Union

from tte_utils.dataset import MyDataset


class RATIO:
    def __init__(self,
                 input_size=1,
                 learning_rate=1e-3):
        self.input_size = input_size
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.network = RATIO_Network(input_size=input_size).to(self.device)
        self.optimizer = torch.optim.Adam(self.network.parameters(), lr=learning_rate)

    def fit(self, x: pd.DataFrame = None, y: pd.DataFrame = None,
            dataset: MyDataset = None,
            n_epochs=1000, batch_size=32, show_progress=True):
        """
        Train the model
        :param x: Dataframe
        :param y: Dataframe
        :param dataset: MyDataset: In case x and y are not provided
        :param n_epochs:
        :param batch_size:
        :param show_progress:
        :return:
        """

        self.network.train()

        # TODO: load coefficients
        if x is not None and y is not None:
            x = torch.from_numpy(x.to_numpy())
            y = torch.from_numpy(y.to_numpy())
            dataset = MyDataset(x, y)
        else:
            x, y = dataset.X, dataset.y

        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        first_loss_history = []
        second_loss_history = []

        for epoch in range(n_epochs):
            # For the first loss
            first_loss_epoch = 0.0
            epoch_first_amount = 0
            # For the second loss
            second_loss_epoch = 0.0
            epoch_second_amount = 0

            for batch_x, batch_y in dataloader:
                batch_x = batch_x.to(self.device)
                batch_y = batch_y.to(self.device)

                self.optimizer.zero_grad()

                output = self.network(batch_x)

                if output.dim() == 0:
                    print("Output is a 0-dimensional tensor.")

                if batch_y.dim() == 0:
                    print("Batch_y is a 0-dimensional tensor.")
                    print("Batch_y: ", batch_y.shape)
                    print("Batch_x: ", batch_x.shape)

                # combined_loss is for back prop, the rest are for logging
                combined_loss, first_loss, batch_first_amount, second_loss, batch_second_amount = RATIO.ratio_loss(
                    y_pred=output, y_true=batch_y)

                combined_loss.backward()
                self.optimizer.step()

                with torch.no_grad():
                    first_loss_epoch += first_loss.item() * batch_first_amount
                    epoch_first_amount += batch_first_amount
                    second_loss_epoch += second_loss.item() * batch_second_amount
                    epoch_second_amount += batch_second_amount

            first_loss_history.append(first_loss_epoch / epoch_first_amount)
            second_loss_history.append(second_loss_epoch / epoch_second_amount)

            if show_progress:
                if epoch % 100 == 0:
                    print(f"Epoch {epoch}, First Loss: {first_loss_epoch / epoch_first_amount}, "
                          f"Second Loss: {second_loss_epoch / epoch_second_amount}")

        return first_loss_history, second_loss_history

    @staticmethod
    def ratio_loss(y_pred, y_true, coefficients=None, device=None):
        if device is None:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        loss_first, loss_second = 0.0, 0.0

        if coefficients is None:
            coefficients = [1.0, 0.5]  # default parameters

        uncensored_idx = y_true[:, 0] == 1
        censored_idx = y_true[:, 0] == 0
        y_cen, y_hat_cen = y_true[censored_idx], y_pred[censored_idx]

        combined_loss = 0.
        # First loss component
        batch_first_amount = uncensored_idx.sum().item()
        if any(uncensored_idx):
            loss_first = F.mse_loss(y_true[uncensored_idx, 1].view(-1, 1), y_pred[uncensored_idx].view(-1, 1),
                                    reduction='mean') * coefficients[0]
            combined_loss += loss_first

        if len(y_cen) == 0:
            if isinstance(combined_loss, float):
                combined_loss = torch.tensor(0., torch.float32, requires_grad=True).to(device)
            return combined_loss

        # Second loss component
        to_change = y_hat_cen.flatten() < y_cen[:, 1].flatten()
        batch_second_amount = to_change.sum().item()
        if any(to_change):
            loss_second = F.mse_loss(y_cen[to_change, 1].view(-1, 1), y_hat_cen[to_change].view(-1, 1)) * coefficients[
                1]
            combined_loss += loss_second

        loss_first = loss_first.item() if not isinstance(loss_first, float) else 0
        loss_second = loss_second.item() if not isinstance(loss_second, float) else 0

        # Last part from ratio
        not_changed = len(y_cen) - sum(to_change)
        if (len(y_pred) - not_changed) != 0:
            combined_loss = (combined_loss * len(y_pred)) / (len(y_pred) - not_changed)

            # Fix loss components accordingly
            loss_first = loss_first * len(y_pred) / (len(y_pred) - not_changed)
            loss_second = loss_second * len(y_pred) / (len(y_pred) - not_changed)

        return combined_loss, loss_first, batch_first_amount, loss_second, batch_second_amount

    def predict(self, x: Union[pd.DataFrame, np.ndarray, torch.Tensor]):
        self.network.eval()
        with torch.no_grad():
            if isinstance(x, pd.DataFrame):
                x = torch.from_numpy(x.to_numpy()).float()
            elif isinstance(x, np.ndarray):
                x = torch.from_numpy(x).float()

            x = x.to(self.device)

            return self.network(x).cpu().detach().numpy()

    def predict_proba(self, x: Union[pd.DataFrame, np.ndarray]):
        raise NotImplementedError("Model does not predict probabilities")


class RATIO_Network(nn.Module):
    def __init__(self, input_size):
        super(RATIO_Network, self).__init__()

        self.input_size = input_size

        self.fc1 = nn.Linear(self.input_size, 1000)
        self.bn1 = nn.BatchNorm1d(1000)
        self.drop1 = nn.Dropout(0.2)
        self.relu1 = nn.ReLU()

        self.fc2 = nn.Linear(1000, 1000)
        self.bn2 = nn.BatchNorm1d(1000)
        self.drop2 = nn.Dropout(0.2)
        self.relu2 = nn.ReLU()

        self.fc3 = nn.Linear(1000, 1)

    def forward(self, x):
        out = self.fc1(x)
        # out = self.bn1(out)
        out = self.relu1(out)
        # out = self.drop1(out)

        out = self.fc2(out)
        # out = self.bn2(out)
        out = self.relu2(out)
        # out = self.drop2(out)

        out = self.fc3(out)

        t = out
        t = F.relu(t)

        return t
