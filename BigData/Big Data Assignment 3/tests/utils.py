import os
import pandas as pd
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def download_online_retail():    
    from ucimlrepo import fetch_ucirepo

    print("Begin Downloading Online Retail Dataset...")
    online_retail = fetch_ucirepo(id=352)
    X = online_retail.data.features
    
    data_dir = 'data' 
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created directory {data_dir}")

    X.to_csv(os.path.join(data_dir, 'Online_Retail_features.csv'), index=False)
    print("Dataset Downloaded and Saved Successfully!")
    
def clean_data():
    print("Begin Cleaning Dataset...")
    data_dir = 'data'
    features_file = os.path.join(data_dir, 'Online_Retail_features.csv')
    df = pd.read_csv(features_file)
    initial_count = len(df)
    print(f"Initial number of rows: {initial_count}")

    # Handling missing values
    df_dropped_na = df.dropna()
    na_dropped_count = initial_count - len(df_dropped_na)
    print(f"Number of rows with missing values dropped: {na_dropped_count}")
    
    # Removing duplicates
    df_deduped = df_dropped_na.drop_duplicates()
    duplicates_dropped_count = len(df_dropped_na) - len(df_deduped)
    print(f"Number of duplicate rows dropped: {duplicates_dropped_count}")

    # Converting data types (e.g., dates)
    df_deduped['InvoiceDate'] = pd.to_datetime(df_deduped['InvoiceDate'], errors='coerce')
    print(f"Date conversion applied to 'InvoiceDate' column.")

    # Save the cleaned data
    cleaned_file = os.path.join(data_dir, 'Online_Retail_features_cleaned.csv')
    df_deduped.to_csv(cleaned_file, index=False)
    final_count = len(df_deduped)
    print(f"Number of rows after cleaning: {final_count}")

    print(f"Cleaned data saved to {cleaned_file}")

def add_total_price():
    print("Adding Total Price Column...")
    data_dir = 'data'
    cleaned_features_file = os.path.join(data_dir, 'Online_Retail_features_cleaned.csv')    
    df = pd.read_csv(cleaned_features_file)
    
    # we round to 2 decimal places because its a currency
    df['TotalPrice'] = (df['Quantity'] * df['UnitPrice']).round(2)
    
    transformed_file = os.path.join(data_dir, 'Online_Retail_features_transformed.csv')
    df.to_csv(transformed_file, index=False)
    
    print(f"Transformed data saved to {transformed_file}")

def load_to_mongodb():
    from pymongo import MongoClient
    mongo_host = 'mongo' # Service name defined in Docker Compose
    mongo_port = 27017
    mongo_db = 'assignment3'
    mongo_collection = 'online_retail'  

    # Connect to MongoDB
    client = MongoClient(host=mongo_host, port=mongo_port, username='mongo_admin', password='password')
    db = client[mongo_db]
    collection = db[mongo_collection]

    # Define the data directory
    data_dir = 'data'
    transformed_features_file = os.path.join(data_dir, 'Online_Retail_features_transformed.csv')

    # Load transformed data
    transformed_df = pd.read_csv(transformed_features_file)

    # Insert transformed data into MongoDB
    records = transformed_df.to_dict(orient='records')
    collection.insert_many(records)

    print(f"Transformed data loaded into MongoDB collection '{mongo_collection}'")

from airflow.utils.email import send_email
from datetime import datetime
def send_summary_email(**kwargs):
    
    dag = kwargs.get('dag')  # Retrieve the DAG object from kwargs
    default_args = dag.default_args  

    # Extract the email address from default_args
    email_to = default_args.get('email')

    task_instance = kwargs['task_instance']
    execution_date = task_instance.execution_date.strftime('%Y-%m-%d %H:%M:%S')
    dag_id = task_instance.dag_id

    subject = f"Airflow Summary: DAG Execution Completed ({dag_id})"
    body = f"DAG {dag_id} execution on {execution_date} completed.\n\n"
    body += "Online Retail Dataset is downloaded, prepared, and ready for Machine Learning tasks.\n\n"

    send_email(email_to, subject, body)