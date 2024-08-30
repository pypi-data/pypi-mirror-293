# utils
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

def check_time_raise_operator(**kwargs):

    # Получите контекст выполнения
    task_instance = kwargs.get('task_instance')  # Объект TaskInstance
    execution_date = kwargs.get('execution_date')  # Дата и время выполнения
    dag = kwargs.get('dag')  # Объект DAG
    dag_id = dag.dag_id if dag else None

    work_day_begin_interval = task_instance.xcom_pull(task_ids='get_config_task', key='work_day_begin_interval')
    work_day_end_interval = task_instance.xcom_pull(task_ids='get_config_task', key='work_day_end_interval')
    check_time_raise(work_day_begin_interval, work_day_end_interval)

def check_time_raise(work_day_begin_interval,work_day_end_interval):
    start_time = datetime.strptime(work_day_begin_interval, '%H:%M:%S').time()
    end_time = datetime.strptime(work_day_end_interval, '%H:%M:%S').time()
    now = datetime.now().time()
    if now < start_time or now > end_time:
        raise ValueError("Task is running outside the allowed time range")
    else:
        print("You work is correctly in the allowed time range between: " + str(work_day_begin_interval) + " - " + str(work_day_end_interval))