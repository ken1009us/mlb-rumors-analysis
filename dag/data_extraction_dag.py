import datetime as dt

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from datetime import datetime
from text_analysis import main


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 25),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}


dag = DAG(
    'mlb_rumors_analysis',
    default_args=default_args,
    description='A DAG to scrape and analyze MLB rumors data',
    schedule_interval=None  # None means it's manually triggered
)


def start_extraction():
    main.start()


start_extraction_task = PythonOperator(
    task_id='run_scraper_and_analysis',
    python_callable=start_extraction,
    dag=dag
)

start_extraction_task
