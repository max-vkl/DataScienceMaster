# test_download_online_retail.py
import os
import pandas as pd
from utils import download_online_retail

def test_download_function():
    # Define the data directory
    data_dir = 'data'
    
    # Remove existing files if any (for a clean test run)
    if os.path.exists(os.path.join(data_dir, 'Online_Retail_features.csv')):
        os.remove(os.path.join(data_dir, 'Online_Retail_features.csv'))
    
    # Call the download function
    download_online_retail()
    
    # Check if the files have been created
    features_file_exists = os.path.exists(os.path.join(data_dir, 'Online_Retail_features.csv'))
    
    # Print results
    if features_file_exists:
        print("Test passed: Files have been created successfully.")
    else:
        print("Test failed: Files have not been created.")
    
    # Optionally, you can load the data and print some information to verify its content
    if features_file_exists:
        features_df = pd.read_csv(os.path.join(data_dir, 'Online_Retail_features.csv'))
        print("Features DataFrame:")
        print(features_df.head())
    

if __name__ == "__main__":
    test_download_function()
