import os
from utils import add_total_price

def test_add_total_price():
    # Define the data directory
    data_dir = 'data'
    
    # Paths to files
    transformed_features_file = os.path.join(data_dir, 'Online_Retail_features_transformed.csv')
    
    # Clean up existing files if any (for a clean test run)
    if os.path.exists(transformed_features_file):
        os.remove(transformed_features_file)
    
    # Call the function to add total price
    add_total_price()
    
    # Check if transformed file has been created
    if os.path.exists(transformed_features_file):
        print("Test passed: Transformed file has been created successfully.")
        
        # Optionally, you can load the transformed data and print some information to verify its content
        import pandas as pd
        transformed_df = pd.read_csv(transformed_features_file)
        print("Transformed DataFrame:")
        print(transformed_df.head())
        assert all((transformed_df['UnitPrice'] * transformed_df['Quantity']).round(2) == transformed_df['TotalPrice'])
    else:
        print("Test failed: Transformed file has not been created.")

if __name__ == "__main__":
    test_add_total_price()
