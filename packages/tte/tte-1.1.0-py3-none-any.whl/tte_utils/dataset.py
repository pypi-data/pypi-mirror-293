import torch
from torch.utils.data import Dataset
import numpy as np


class MyDataset(Dataset):

    def __init__(self, X, y, is_train=True, mu=None, sigma=None):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        X = X.to_numpy()  # size: (n_samples, n_features)
        y = y.to_numpy()  # size: (n_samples, 2): first column is the event time, second column is the event type

        X = torch.from_numpy(X.astype(np.float32)).to(self.device)
        y = torch.from_numpy(y.astype(np.float32)).to(self.device)

        self.X = X
        self.y = y

        # scale the features, if is_train=True, calculate mu and sigma, else use the given mu and sigma
        # if is_train:
        #     self.mu = X.mean(0, keepdim=True)
        #     self.sigma = X.std(0, unbiased=False, keepdim=True)
        #     self.X = (X - self.mu) / self.sigma
        # else:
        #     self.mu = mu
        #     self.sigma = sigma
        #     self.X = (X - self.mu) / self.sigma
        self.n_samples = X.shape[0]

    def __getitem__(self, index):
        return self.X[index], self.y[index]

    def __len__(self):
        return self.n_samples

    @staticmethod
    def is_censored(y):
        """
        :return: all the samples
        """
        if len(y.shape) == 1:
            val = y[0] == 0.0
            return torch.tensor([val])
        return y[:, 0] == 0.0

    @staticmethod
    def is_uncensored(y):
        """
        :return: all the samples
        """
        if len(y.shape) == 1:
            val = y[0] != 0.0
            return torch.tensor([val])
        return y[:, 0] != 0.0

    @staticmethod
    def get_time(y, device=None):
        # either the event time or the censored time, depends on the event type
        if len(y.shape) == 1:
            val = y[0]
            if device is None:
                device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            return torch.tensor([val]).to(device)
        return y[:, 1]
