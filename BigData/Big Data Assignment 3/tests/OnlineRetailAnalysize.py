from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from utils import *

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 27),
    'email_on_failure': True,
    'email': 'jfcplayer66@googlemail.com', # add your email here
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Define the DAG
dag = DAG(
    'download_online_retail',
    default_args=default_args,
    description='Download Online Retail dataset from UCI Machine Learning Repository using ucimlrepo',
    schedule_interval='@daily',
)

def throw_error():
    raise Exception("Example exception to simulate failure. This mail contains the error description and link to the Log of the task in the Airflow UI.")

task_with_error = PythonOperator(
    task_id='task_with_error',
    python_callable=throw_error,
    dag=dag,
)

pip_install_task = BashOperator(
    task_id='install_libraries',
    bash_command="pip install ucimlrepo pymongo",
    dag=dag,
)

download_task = PythonOperator(
    task_id='download_online_retail_task',
    python_callable=download_online_retail,
    dag=dag,
)

clean_data_task = PythonOperator(
    task_id='clean_data_task',
    python_callable=clean_data,
    dag=dag,
)

transform_data_task = PythonOperator(
    task_id='transform_data_task',
    python_callable=add_total_price,
    dag=dag,
)

load_to_mongodb_task = PythonOperator(
        task_id='load_to_mongodb_task',
        python_callable=load_to_mongodb,
        dag=dag,
    )

send_summary_email_task = PythonOperator(
    task_id='send_summary_email_task',
    python_callable=send_summary_email,
    provide_context=True,
    dag=dag,
)

# Set the task dependencies
pip_install_task>>download_task>>clean_data_task>>transform_data_task>>load_to_mongodb_task >> send_summary_email_task>>task_with_error
