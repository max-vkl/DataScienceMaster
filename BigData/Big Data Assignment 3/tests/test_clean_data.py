import os
import pandas as pd
from utils import download_online_retail, clean_data

def test_clean_function():
    # Define the data directory
    data_dir = 'data'
    raw_features_file = os.path.join(data_dir, 'Online_Retail_features.csv')
    cleaned_features_file = os.path.join(data_dir, 'Online_Retail_features_cleaned.csv')
    
    # Ensure the raw data file exists by calling the download function
    if not os.path.exists(raw_features_file):
        download_online_retail()
    
    # Check if the raw features file was created
    if not os.path.exists(raw_features_file):
        print("Test failed: Raw features file does not exist.")
        return
    
    # Call the clean function
    clean_data()
    
    # Check if the cleaned file has been created
    cleaned_file_exists = os.path.exists(cleaned_features_file)
    
    # Print results
    if cleaned_file_exists:
        print("Test passed: Cleaned file has been created successfully.")
        
        # Optionally, you can load the cleaned data and print some information to verify its content
        cleaned_df = pd.read_csv(cleaned_features_file)
        print("Cleaned DataFrame:")
        print(cleaned_df.head())
    else:
        print("Test failed: Cleaned file has not been created.")
    
    # Additional verification steps
    if cleaned_file_exists:
        cleaned_df = pd.read_csv(cleaned_features_file)
        print(f"Number of rows in cleaned data: {len(cleaned_df)}")
        print(f"Columns in cleaned data: {list(cleaned_df.columns)}")

if __name__ == "__main__":
    test_clean_function()
