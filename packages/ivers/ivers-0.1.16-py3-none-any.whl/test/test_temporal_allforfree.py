import unittest
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from typing import List, Tuple
from ivers.temporal import allforfree_endpoint_split, allforfree_folds_endpoint_split
import os
class TestAllForFreeFoldsEndpointSplit(unittest.TestCase):
    def setUp(self):
        """Set up the DataFrame and parameters for the tests."""
        self.data = {
            'SMILES': ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8'],
            'Activity_Date': [datetime(2020, 1, 1), datetime(2020, 2, 1), datetime(2020, 3, 1), datetime(2020, 4, 1), 
                              datetime(2020, 5, 1), datetime(2020, 6, 1), datetime(2020, 7, 1), datetime(2020, 8, 1)],
            'Activity': [1, 2, 3, 4, 5, 6, 7, 8],
            'Feature_1': [10, 20, 30, 40, 50, 60, 70, 80],
            'Feature_2': [100, 200, 300, 400, 500, 600, 700, 800]
        }
        self.df = pd.DataFrame(self.data)
        self.num_folds = 3
        self.smiles_column = 'SMILES'
        self.endpoint_date_columns = {'Activity': 'Activity_Date'}
        self.exclude_columns = ['Feature_2']
        self.chemprop = False
        self.save_path = './'

    def tearDown(self):
        """Remove all .csv files after the test is done."""
        for file in os.listdir(self.save_path):
            if file.endswith(".csv"):
                os.remove(os.path.join(self.save_path, file))
                print(f"Deleted file: {file}")

    def test_splits(self):
        """Test the training/test splits to ensure proper handling."""
        # Execute the function
        result = allforfree_folds_endpoint_split(
            self.df, self.num_folds, self.smiles_column, self.endpoint_date_columns,
            self.exclude_columns, self.chemprop, self.save_path
        )

        # Assert the results
        self.assertEqual(len(result), self.num_folds, "Incorrect number of folds returned.")
        previous_test_len = len(self.df)
        for i, (train, test) in enumerate(result):
            current_test_len = len(test)
            self.assertTrue(current_test_len < previous_test_len, f"Test set size did not decrease from fold {i} to fold {i+1}")
            self.assertTrue(current_test_len > 0, f"Test set size is 0 for fold {i+1}")
            previous_test_len = current_test_len

if __name__ == '__main__':
    unittest.main()
