import numpy as np
import torch.nn as nn
import torch
import torch.nn.functional as F
import pandas as pd
from torch.utils.data import DataLoader
from typing import Union

from tte_utils.dataset import MyDataset


class MyModel:
    def __init__(self,
                 input_size=1,
                 learning_rate=1e-3):
        self.input_size = input_size
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.network = TwoNetworks(input_size=input_size).to(self.device)
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
        third_loss_history = []

        uncensored_mean = np.mean(y[y[:, 0] == 1][:, 1]).to(self.device)
        # calculate the mean y value of the censored samples
        censored_mean = np.mean(y[y[:, 0] == 0][:, 1]).to(self.device)

        for epoch in range(n_epochs):
            # For the first loss
            first_loss_epoch = 0.0
            epoch_first_amount = 0
            # For the second loss
            second_loss_epoch = 0.0
            epoch_second_amount = 0
            # For the third loss
            third_loss_epoch = 0.0
            epoch_third_amount = 0

            for batch_x, batch_y in dataloader:
                batch_x = batch_x.to(self.device)
                batch_y = batch_y.to(self.device)

                self.optimizer.zero_grad()

                t_pred, p_pred = self.network(batch_x)

                # combined_loss is for back prop, the rest are for logging
                (combined_loss, first_loss, batch_first_amount, second_loss, batch_second_amount,
                 third_loss, batch_third_amount) = MyModel.my_loss(
                    t_pred, p_pred, y_true=batch_y,
                    uncensored_mean=uncensored_mean,
                    censored_mean=censored_mean)

                combined_loss.backward()
                self.optimizer.step()

                with torch.no_grad():
                    first_loss_epoch += first_loss.item() * batch_first_amount
                    epoch_first_amount += batch_first_amount

                    second_loss_epoch += second_loss.item() * batch_second_amount
                    epoch_second_amount += batch_second_amount

                    third_loss_epoch += third_loss.item() * batch_third_amount
                    epoch_third_amount += batch_third_amount

            first_loss_history.append(first_loss_epoch / epoch_first_amount)
            second_loss_history.append(second_loss_epoch / epoch_second_amount)
            third_loss_history.append(third_loss_epoch / epoch_third_amount)

            if show_progress:
                if epoch % 100 == 0:
                    print(f"Epoch {epoch}, First Loss: {first_loss_epoch / epoch_first_amount}, "
                          f"Second Loss: {second_loss_epoch / epoch_second_amount}")

        return first_loss_history, second_loss_history, third_loss_history

    @staticmethod
    def my_loss(t_pred, p_pred, y_true, uncensored_mean, censored_mean, coefficients=None, device=None):
        if device is None:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        loss_first, loss_second, loss_third = 0.0, 0.0, 0.0

        if coefficients is None:
            coefficients = [100.0, 31.2, 0.5]  # default parameters

        uncensored_idx = y_true[:, 0] == 1
        censored_idx = y_true[:, 0] == 0

        combined_loss = 0.
        # if it remains zero, then loss is a float and will get converted to a tensor
        is_zero = True

        # First loss component: MSE loss for uncensored samples
        batch_first_amount = uncensored_idx.sum().item()
        if any(uncensored_idx):
            is_zero = False
            loss_first = F.mse_loss(y_true[uncensored_idx, 1].view(-1, 1), t_pred[uncensored_idx].view(-1, 1),
                                    reduction='mean') * coefficients[0]
            first_normalization = torch.sum(
                torch.square(MyDataset.get_time(y_true)[uncensored_idx].view(-1, 1) - uncensored_mean))
            loss_first /= first_normalization
            combined_loss += loss_first

        # Second loss component: negative log likelihood for uncensored samples
        batch_second_amount = uncensored_idx.sum().item()
        if any(uncensored_idx):
            loss_second = - torch.mean(torch.log(p_pred[uncensored_idx].view(-1, 1))) * coefficients[1]
        else:
            loss_second = torch.tensor(data=0., dtype=torch.float32, requires_grad=True)

        combined_loss += loss_second

        # calculate sum over the censored where we estimated lower than the censoring time: (t_pred - t_censored)^2 * p_pred
        # get the indices of the censored samples where the predicted time is lower than the censoring time
        to_change_idx = t_pred.flatten() < MyDataset.get_time(y_true).flatten()
        to_change_idx = to_change_idx & censored_idx

        batch_third_amount = to_change_idx.sum().item()
        if any(to_change_idx):
            is_zero = False

            first_term = torch.square(
                t_pred[to_change_idx].view(-1, 1) - MyDataset.get_time(y_true)[to_change_idx].view(-1, 1))
            second_term = p_pred[to_change_idx].view(-1, 1)

            loss_third = torch.mean(torch.mul(first_term, second_term)) * coefficients[2]
            third_normalization = torch.sum(
                torch.square(MyDataset.get_time(y_true)[censored_idx].view(-1, 1) - censored_mean))
            loss_third /= third_normalization

        if is_zero:
            combined_loss = torch.tensor(data=0., dtype=torch.float32, requires_grad=True).to(device)
            return combined_loss

        return combined_loss, loss_first, batch_first_amount, loss_second, batch_second_amount, loss_third, batch_third_amount

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
        raise NotImplementedError("predict_proba is not implemented")


class TwoNetworks(nn.Module):
    def __init__(self, input_size):
        super(TwoNetworks, self).__init__()

        self.input_size = input_size

        self.t_fc1 = nn.Linear(self.input_size, 1000)
        # self.t_bn1 = nn.BatchNorm1d(1000)
        # self.t_drop1 = nn.Dropout(0.2)
        self.t_relu1 = nn.ReLU()

        self.t_fc2 = nn.Linear(1000, 1000)
        # self.t_bn2 = nn.BatchNorm1d(1000)
        # self.t_drop2 = nn.Dropout(0.2)
        self.t_relu2 = nn.ReLU()

        self.t_fc3 = nn.Linear(1000, 1)

        self.p_fc1 = nn.Linear(self.input_size, 1000)
        # self.p_bn1 = nn.BatchNorm1d(1000)
        # self.p_drop1 = nn.Dropout(0.2)
        self.p_relu1 = nn.ReLU()

        self.p_fc2 = nn.Linear(1000, 1000)
        # self.p_bn2 = nn.BatchNorm1d(1000)
        # self.p_drop2 = nn.Dropout(0.2)
        self.p_relu2 = nn.ReLU()

        self.p_fc3 = nn.Linear(1000, 1)

    def forward(self, x):
        t = self.t_fc1(x)
        t = self.t_relu1(t)
        t = self.t_fc2(t)
        t = self.t_relu2(t)
        t = self.t_fc3(t)
        t = F.relu(t)

        p = self.p_fc1(x)
        p = self.p_relu1(p)
        p = self.p_fc2(p)
        p = self.p_relu2(p)
        p = self.p_fc3(p)
        p = torch.sigmoid(p)

        return t, p

    def _common_step(self, x):
        out = self.fc1(x)
        # out = self.bn1(out)
        out = self.relu1(out)
        # out = self.drop1(out)

        out = self.fc2(out)
        # out = self.bn2(out)
        out = self.relu2(out)
        # out = self.drop2(out)
        out = self.fc3(out)
        return out
