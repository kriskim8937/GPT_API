from datetime import datetime
from pprint import pprint
from airflow import DAG
from airflow.decorators import task

# Define the default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 1),
    'retries': 1,
}

# Define the DAG
dag = DAG(
    'example_dag',
    default_args=default_args,
    description='An example DAG using task decorator',
    schedule_interval="@daily",
)

# Define the task using the @task decorator
@task(task_id="print_the_context", dag=dag)
def print_context(ds=None, **kwargs):
    """Print the Airflow context and ds variable from the context."""
    pprint(kwargs)
    print(ds)
    return "Whatever you return gets printed in the logs"

# Assign the task to a variable
run_this = print_context()

# Optionally, define any task dependencies using the >> or << operators
# run_this_2 = another_task_function()
# run_this >> run_this_2

if __name__ == "__main__":
    dag.cli()