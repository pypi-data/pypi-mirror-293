from SurvSet.data import SurvLoader
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.utils import shuffle

from tte_utils.dataset import MyDataset


def load_dataset(dataset_name: str):
    """
    :param dataset_name:
    :return: Dataframe, reference to the dataset
    """
    loader = SurvLoader()
    df, ref = loader.load_dataset(ds_name=dataset_name).values()
    return df, ref


def preprocess_and_split(df: pd.DataFrame, perform_z_score: bool = False):
    """
    Preprocess the data
    :param df: dataframe
    :param perform_z_score: boolean
    :return: preprocessed dataframe
    """

    # drop pid column
    df = df.drop(['pid'], axis=1)

    df = shuffle(df, random_state=42)
    df.reset_index(drop=True, inplace=True)

    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

    for train_index, test_index in split.split(df, df['event']):
        df_train, df_test = df.iloc[train_index], df.iloc[test_index]

    # Define transformers for categorical and numerical features
    categorical_features = df.columns[df.columns.str.startswith('fac')]
    numerical_features = df.columns[df.columns.str.startswith('num')]
    unchanged_features = ['event', 'time']

    # Pipeline for categorical features (Imputation + OneHotEncoding)
    categorical_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent', missing_values=None)),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    # Pipeline for numerical features (Imputation + Z-score scaling)
    numerical_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean'))
    ])

    # Combine pipelines using ColumnTransformer
    preprocessor = ColumnTransformer([
        ('cat', categorical_pipeline, categorical_features),
        ('num', numerical_pipeline, numerical_features),
        ('unchanged', 'passthrough', unchanged_features)
    ])

    # Full pipeline with missing value handling and preprocessing
    full_pipeline = Pipeline([
        ('missing_handler', MissingValueHandler(df=df_train)),
        ('preprocessor', preprocessor),
    ])

    # Fit-transform the train data
    transformed_data_train = full_pipeline.fit_transform(df_train)

    # Get the feature names after transformation
    if len(categorical_features) > 0:
        categorical_feature_names = full_pipeline.named_steps['preprocessor'].named_transformers_['cat'][
            'onehot'].get_feature_names_out(categorical_features)
        categorical_feature_names = list(categorical_feature_names)
    else:
        categorical_feature_names = []
    numerical_feature_names = numerical_features
    all_feature_names = list(categorical_feature_names) + list(numerical_feature_names) + unchanged_features

    # Convert to DataFrame
    transformed_df_train = pd.DataFrame(transformed_data_train, columns=all_feature_names)

    # print(transformed_df_train)

    # Transform the test data
    transformed_data_test = full_pipeline.transform(df_test)
    transformed_df_test = pd.DataFrame(transformed_data_test, columns=all_feature_names)
    # print(transformed_df_test)
    if perform_z_score:
        features_to_normalize = transformed_df_train.columns[transformed_df_train.columns.str.startswith('num') + transformed_df_train.columns.str.startswith('time')]
        transformed_df_train, numerical_pipeline = perform_z_score_on_numerical_features(transformed_df_train, features_to_normalize)
        transformed_df_test[features_to_normalize] = numerical_pipeline.transform(transformed_df_test[features_to_normalize])

    X_train = transformed_df_train.drop(['event', 'time'], axis=1)
    y_train = transformed_df_train[['event', 'time']]

    X_test = transformed_df_test.drop(['event', 'time'], axis=1)
    y_test = transformed_df_test[['event', 'time']]

    train_dataset = MyDataset(X_train, y_train)
    test_dataset = MyDataset(X_test, y_test)

    return train_dataset, test_dataset


def perform_z_score_on_numerical_features(df: pd.DataFrame, features_to_normalize):
    """
    Perform Z-score scaling on numerical features
    :param df: dataframe
    :return: scaled dataframe
    """
    numerical_pipeline = Pipeline([
        ('scaler', StandardScaler())
    ])

    df[features_to_normalize] = numerical_pipeline.fit_transform(df[features_to_normalize])

    return df, numerical_pipeline


class MissingValueHandler(BaseEstimator, TransformerMixin):
    def __init__(self, df, threshold=0.5):
        self.threshold = threshold
        self.df = df

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        amount_of_rows_with_missing_values = self.df.isnull().any(axis=1).sum()
        missing_ratio = amount_of_rows_with_missing_values / self.df.shape[0]
        # print(f'Missing ratio: {missing_ratio}')
        # print(f'Threshold: {self.threshold}')
        if missing_ratio > self.threshold:
            return X.dropna()
        else:
            return X
