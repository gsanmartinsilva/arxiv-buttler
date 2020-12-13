
from datetime import timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to operate!
from airflow.operators.docker_operator import DockerOperator
from airflow.utils.dates import days_ago
from airflow.utils import timezone

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(0),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(seconds=5),
}
dag = DAG(
    'arxiv-data-collector',
    default_args=default_args,
    description='DAG that collects and download arxiv data',
    schedule_interval='0 * * * *',
    tags=['arxiv-buttler'],
    catchup=False 
)

# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = DockerOperator(
    task_id='fetch_and_load',
    image='arxiv',
    dag=dag,
    auto_remove=True,
    container_name='arxiv-buttler_data_capture',
    command='python /home/arxiv-buttler/fetch_and_load.py',
    volumes=['/home/gsanm/arxiv-buttler:/home/arxiv-buttler']
)

t2 = DockerOperator(
    task_id='download_txt',
    image='arxiv',
    dag=dag,
    auto_remove=True,
    container_name='arxiv-buttler_download_pdf',
    command='python /home/arxiv-buttler/download_pdf.py',
    volumes=['/home/gsanm/arxiv-buttler:/home/arxiv-buttler']
)


t1 >> t2

