# dags/generate_report_dag.py
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import os

def generate_report():
    report_path = '/opt/airflow/reports/report.txt'
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w') as f:
        f.write('This is a sample report.\n')
        f.write('Generated by Airflowssssssssssssssssssssssssssssss.')

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'generate_report_dag',
    default_args=default_args,
    description='A simple report generation DAG',
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

generate_report_task = PythonOperator(
    task_id='generate_report',
    python_callable=generate_report,
    dag=dag,
)