from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from datetime import datetime
from text_analysis import data_extraction


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 10, 24),
}


dag = DAG(
    'data_extraction',
    default_args=default_args,
    description='DAG for extracting MLB rumors data',
    schedule_interval=None  # None means it's manually triggered
)


def start_extraction():
    data_extraction.start()


start_extraction_task = PythonOperator(
    task_id='start_extraction_task',
    python_callable=start_extraction,
    dag=dag
)