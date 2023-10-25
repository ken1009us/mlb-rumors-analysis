import datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from data_analysis import main


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.datetime(2023, 10, 25),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5),
}


dag = DAG(
    dag_id='mlb_rumors_analysis',
    default_args=default_args,
    description='A DAG to scrape and analyze MLB rumors data',
    schedule_interval=None
)


start_extraction_task = PythonOperator(
    task_id='run_scraper_and_analysis',
    python_callable=main,
    dag=dag
)


if __name__ == "__main__":
    dag.cli()
