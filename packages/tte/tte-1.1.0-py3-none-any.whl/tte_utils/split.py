from sklearn.utils import shuffle
from sklearn.model_selection import StratifiedShuffleSplit
import pandas as pd
from tte_utils.dataset import MyDataset


def train_val_test_split(df: pd.DataFrame):
    """
    Split the data into train, validation and test sets
    :param df: dataframe
    :return: train, validation and test dataset
    """
    df = shuffle(df, random_state=42)
    df.reset_index(drop=True, inplace=True)
    X = df.drop(['pid', 'event', 'time'], axis=1)
    y = df[['event', 'time']]

    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

    # reset index so that stratified shuffle split will work
    df.reset_index(drop=True, inplace=True)

    for dev_index, test_index in split.split(df, df['event']):
        X_dev, X_test = X.iloc[dev_index], X.iloc[test_index]
        y_dev, y_test = y.iloc[dev_index], y.iloc[test_index]

    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

    # concat X_dev and y_dev
    df_dev = pd.concat([X_dev, y_dev], axis=1)

    for train_index, val_index in split.split(df_dev, df_dev['event']):
        X_train, X_val = X_dev.iloc[train_index], X_dev.iloc[val_index]
        y_train, y_val = y_dev.iloc[train_index], y_dev.iloc[val_index]

    train_dataset = MyDataset(X_train, y_train)
    val_dataset = MyDataset(X_val, y_val)
    test_dataset = MyDataset(X_test, y_test)

    return train_dataset, val_dataset, test_dataset


def train_test_split(df: pd.DataFrame):
    """
    Split the data into train, validation and test sets
    :param df: dataframe
    :return: train and test dataset
    """
    df = shuffle(df, random_state=42)
    df.reset_index(drop=True, inplace=True)
    X = df.drop(['pid', 'event', 'time'], axis=1)
    y = df[['event', 'time']]

    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

    # reset index so that stratified shuffle split will work
    df.reset_index(drop=True, inplace=True)

    for train_index, test_index in split.split(df, df['event']):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

    train_dataset = MyDataset(X_train, y_train)
    test_dataset = MyDataset(X_test, y_test)

    return train_dataset, test_dataset