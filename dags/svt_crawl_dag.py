# airflow_dag.py

from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import task
from pprint import pprint
from src.svt_video_generator import SvtVideoGenerator
from src.svt_parser import SvtParser

# Function to crawl posts from a website
@task(task_id="crawl_posts_task")
def crawl_posts():
    svt_video_generator = SvtVideoGenerator(SvtParser())
    svt_video_generator.crawl_contents()

@task(task_id="print_the_context")
def print_context(ds=None, **kwargs):
    """Print the Airflow context and ds variable from the context."""
    pprint(kwargs)
    print(ds)
    return "Whatever you return gets printed in the logs"

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'crawl_posts_dag',
    default_args=default_args,
    description='A simple DAG to crawl posts from a website',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    # Define the tasks
    crawl_posts_task = crawl_posts()
    print_context_task = print_context()

    # Set task dependencies
    crawl_posts_task >> print_context_task
