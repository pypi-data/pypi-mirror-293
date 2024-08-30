import pandas as pd
from pandas import DataFrame
import logging
from typing import Tuple, List, Dict
import numpy as np
import os
# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_aggregation_rules(df: DataFrame, exclude_columns: List[str]) -> dict:
    """
    Determine aggregation rules for the DataFrame columns based on their data types.
    """
    return {col: ('mean' if df[col].dtype in [np.float64, np.int64] else 'first')
            for col in df.columns if col not in exclude_columns}


def allforfree_endpoint_split(df_list: List[pd.DataFrame], split_size: float, smiles_column: str,
                              endpoint_date_columns: Dict[str, str], aggregation: str, exclude_columns: List[str] =[]) -> Tuple[List[pd.DataFrame], List[pd.DataFrame]]:
    """
    Splits multiple DataFrames containing chemical compound data into training and testing datasets based on specified aggregation
    of dates across given endpoints.

    Parameters:
        df_list (List[pd.DataFrame]): List of DataFrames to be split.
        split_size (float): Fraction of data to use as the test set.
        smiles_column (str): Column name for the compound identifiers (SMILES).
        endpoint_date_columns (Dict[str, str]): Dictionary mapping endpoint names to their date column names.
        aggregation (str): Method of date aggregation ('min', 'max', 'avg').

    Returns:
        Tuple[List[pd.DataFrame], List[pd.DataFrame]]: Tuple containing lists of training and testing DataFrames.
    """
    all_test_compounds = set()
    compound_dates = {}

    # Iterate over each DataFrame and corresponding endpoint date column
    for df, (endpoint, date_column) in zip(df_list, endpoint_date_columns.items()):
        df[date_column] = pd.to_datetime(df[date_column])
        grouped = df.groupby(smiles_column)[date_column]

        if aggregation == 'min':
            aggregated_dates = grouped.min()
        elif aggregation == 'max':
            aggregated_dates = grouped.max()
        elif aggregation == 'avg':
            aggregated_dates = grouped.mean()
        else:
            raise ValueError("Invalid aggregation method. Use 'min', 'max', or 'avg'.")

        for compound, date in aggregated_dates.items():
            compound_dates[compound] = date

    # Determine test compounds based on sorted aggregated dates
    sorted_compounds = sorted(compound_dates.items(), key=lambda x: x[1], reverse=(aggregation != 'min'))
    num_test_compounds = int(len(sorted_compounds) * split_size)
    all_test_compounds.update([comp for comp, _ in sorted_compounds[:num_test_compounds]])

    # Create initial splits
    train_dfs, test_dfs = [], []
    for df in df_list:
        df_test = df[df[smiles_column].isin(all_test_compounds)]
        df_train = df[~df[smiles_column].isin(all_test_compounds)]
        train_dfs.append(df_train)
        test_dfs.append(df_test)
        
    # Concatenate all training and testing DataFrames
    all_train_df = pd.concat(train_dfs, axis=0, ignore_index=True, sort=False)
    all_test_df = pd.concat(test_dfs, axis=0, ignore_index=True, sort=False)

    # Aggregation rules to apply
    aggregation_rules = {col: 'mean' if df[col].dtype in [np.float64, np.int64] and col not in exclude_columns and col != smiles_column 
                else 'first' for col in df.columns}
    aggregation_rules.update(aggregation_rules)

    # Group by SMILES and apply aggregation
    all_train_df = all_train_df.groupby(smiles_column, as_index=False).agg(aggregation_rules)
    all_test_df = all_test_df.groupby(smiles_column, as_index=False).agg(aggregation_rules)

    return all_train_df, all_test_df




def allforfree_folds_endpoint_split(df: pd.DataFrame, num_folds: int, smiles_column: str, endpoint_date_columns: Dict[str, str], exclude_columns: List[str], chemprop: bool, save_path: str, aggregation: str) -> List[Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Process a DataFrame by splitting it into multiple train/test sets for cross-validation, with the training set growing progressively.
    
    Args:
        df: DataFrame to be processed.
        num_folds: Number of folds for cross-validation.
        smiles_column: Name of the column containing compound identifiers.
        endpoint_date_columns: Dictionary of endpoint names to their respective date columns.
        exclude_columns: List of columns to exclude from aggregation rules.
        chemprop: Boolean to indicate if data is for chemprop.
        save_path: Path to save the resulting dataframes.
        aggregation: min or max

    Returns:
        List of tuples containing training and testing DataFrames for each fold.
    """
    if aggregation not in ['min', 'max', 'avg']:
        raise ValueError("Aggregation method must be 'min', 'max', or 'avg'.")
    cv_splits = []
    for fold in range(1, num_folds + 1):
        split_size = 1 - (fold / (num_folds + 1))  # Decrease the test size progressively
        
        train_df, test_df = allforfree_endpoint_split(df, split_size, smiles_column, endpoint_date_columns, aggregation, exclude_columns)
        
        if chemprop:
            feature_columns = [col for col in df.columns if col not in [smiles_column, *endpoint_date_columns.keys(), *endpoint_date_columns.values(), *exclude_columns]]
            train_features = extract_features(train_df, smiles_column, feature_columns)
            test_features = extract_features(test_df, smiles_column, feature_columns)
            train_targets = train_df[list(endpoint_date_columns.keys())]
            test_targets = test_df[list(endpoint_date_columns.keys())]

            # Save features and targets
            train_features.to_csv(os.path.join(save_path, f'train_features_fold{fold}.csv'), index=False)
            test_features.to_csv(os.path.join(save_path, f'test_features_fold{fold}.csv'), index=False)
            train_targets.to_csv(os.path.join(save_path, f'train_targets_fold{fold}.csv'), index=False)
            test_targets.to_csv(os.path.join(save_path, f'test_targets_fold{fold}.csv'), index=False)
        else:
            # print type 
            train_df.to_csv(os.path.join(save_path, f'train_fold{fold}.csv'), index=False)
            test_df.to_csv(os.path.join(save_path, f'test_fold{fold}.csv'), index=False)

        cv_splits.append((train_df, test_df))

    return cv_splits

def leaky_endpoint_split(df: DataFrame, split_size: float, smiles_column: str, endpoint_date_columns: Dict[str, str], exclude_columns: List[str]) -> Tuple[DataFrame, DataFrame]:
    """
    Process a DataFrame by identifying test compounds and splitting the DataFrame for multiple endpoints each with its own date column.

    Args:
        df: DataFrame to be processed.
        split_size: Fraction of the DataFrame to include in the test set for each endpoint.
        smiles_column: Name of the column containing compound identifiers.
        endpoint_date_columns: Dictionary of endpoint names to their respective date columns.

    Returns:
        Tuple containing the training and testing DataFrames.
    """
    
    test_compounds_by_endpoint = {}
    all_test_compounds = set()
    
    # Identify test compounds for each endpoint
    for endpoint, date_column in endpoint_date_columns.items():
        value_column = endpoint  # Assuming the value column has the same name as the endpoint
        # Filter to include only non-null dates and non-null endpoint values
        df_filtered = df[df[date_column].notnull() & df[value_column].notnull()]
        df_sorted = df_filtered.sort_values(by=date_column, ascending=False)
        
        test_size = int(len(df_sorted) * split_size)
        new_test_compounds = set(df_sorted.iloc[:test_size][smiles_column].unique())
        all_test_compounds.update(new_test_compounds)
        test_compounds_by_endpoint[endpoint] = new_test_compounds

    train_dfs = []
    test_dfs = []

    # Split the DataFrame into training and testing sets for each endpoint
    for endpoint in endpoint_date_columns.keys():
        test_compounds = test_compounds_by_endpoint[endpoint]
        # Filter test set to include only those rows with non-null endpoint values
        test_df = df[df[smiles_column].isin(test_compounds) & df[endpoint].notnull()]
        train_df = df[~df[smiles_column].isin(test_compounds) | df[endpoint].isnull()]
        train_dfs.append(train_df)
        test_dfs.append(test_df)


    # Concatenate all training and testing DataFrames
    all_train_df = pd.concat(train_dfs, axis=0, ignore_index=True, sort=False)
    all_test_df = pd.concat(test_dfs, axis=0, ignore_index=True, sort=False)

    # Aggregation rules to apply
    aggregation_rules = {col: 'mean' if df[col].dtype in [np.float64, np.int64] and col not in exclude_columns and col != smiles_column 
                else 'first' for col in df.columns}
    aggregation_rules.update(aggregation_rules)

    # Group by SMILES and apply aggregation
    all_train_df = all_train_df.groupby(smiles_column, as_index=False).agg(aggregation_rules)
    all_test_df = all_test_df.groupby(smiles_column, as_index=False).agg(aggregation_rules)

    return all_train_df, all_test_df

# ------------------------------------ #
# with chemprop compatibility          #
# ------------------------------------ #
def extract_features(df: pd.DataFrame, smiles_column: str, feature_columns: List[str]) -> pd.DataFrame:
    """
    Extract features from the DataFrame.

    Args:
        df: The original DataFrame.
        smiles_column: Column name containing the SMILES strings.
        feature_columns: List of columns to be used as features.

    Returns:
        A DataFrame containing the SMILES and features.
    """
    return df[[smiles_column] + feature_columns]

def leaky_folds_endpoint_split(df: DataFrame, num_folds: int, smiles_column: str, endpoint_date_columns: Dict[str, str], exclude_columns: List[str], chemprop: bool, save_path: str, feature_columns: List[str] = None) -> List[Tuple[DataFrame, DataFrame]]:
    """
    Process a DataFrame by splitting it into multiple train/test sets for cross-validation, with the training set growing progressively.
    The size of the test set decreases with each fold, increasing the training data size.

    Args:
        df: DataFrame to be processed.
        num_folds: Number of folds for cross-validation.
        smiles_column: Name of the column containing compound identifiers.
        endpoint_date_columns: Dictionary of endpoint names to their respective date columns.
        chemprop: Boolean to indicate if data is for chemprop.
        save_path: Path to save the resulting dataframes.
        feature_columns: List of columns to be used as features. If None, exclude_columns will be used.

    Returns:
        List of tuples containing training and testing DataFrames for each fold.
    """
    splits = []

    # test comment
    for fold in range(1, num_folds + 1 ):
        print(f'Processing fold {fold} of {num_folds}')
        split_size = 1 - (fold / (num_folds + 1))  # Decrease the test size progressively
        
        # Use the leaky_endpoint_split function to generate each fold's split
        train_df, test_df = leaky_endpoint_split(df, split_size, smiles_column, endpoint_date_columns, exclude_columns)
        
        if chemprop:
            if feature_columns is None:
                feature_columns = [col for col in df.columns if col not in [smiles_column, *endpoint_date_columns.keys(), *endpoint_date_columns.values(), *exclude_columns]]
            train_features = extract_features(train_df, smiles_column, feature_columns)
            test_features = extract_features(test_df, smiles_column, feature_columns)
            train_targets = train_df[list(endpoint_date_columns.keys())]
            test_targets = test_df[list(endpoint_date_columns.keys())]

            # Save features and targets
            train_features.to_csv(os.path.join(save_path, f'train_features_fold{fold}.csv'), index=False)
            test_features.to_csv(os.path.join(save_path, f'test_features_fold{fold}.csv'), index=False)
            train_targets.to_csv(os.path.join(save_path, f'train_targets_fold{fold}.csv'), index=False)
            test_targets.to_csv(os.path.join(save_path, f'test_targets_fold{fold}.csv'), index=False)
        else:
            train_df.to_csv(os.path.join(save_path, f'train_fold{fold}.csv'), index=False)
            test_df.to_csv(os.path.join(save_path, f'test_fold{fold}.csv'), index=False)

        splits.append((train_df, test_df))

    return splits