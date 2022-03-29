import datetime

from airflow import models
from airflow.contrib.operators.dataflow_operator import DataflowTemplateOperator
from airflow.utils.dates import days_ago
\

bucket_path = 'rg-acp-storage'
project_id = 'shaped-icon-344520'
gce_zone = 'us-central1-a'


default_args = {
    'start_date': days_ago(1),
    'dataflow_default_options': {
        'project': project_id,
        'zone': gce_zone,
        'tempLocation': f'gs://{bucket_path}/airflow-tmp/'
    },
}

with models.DAG(
    'raw_layer',
    default_args=default_args,
    schedule_interval=None,
) as dag:
    dataflow_template_op = DataflowTemplateOperator(
        task_id='movie-review-gcs-csv-to-bq',
        retries=0,
        template=f'gs://{bucket_path}/templates/raw_movie_review_gcs_csv_to_bq',
        job_name='gcs-csv-to-bq-movie-review',
        parameters={'input': f'gs://{bucket_path}/data/movie_review_minimal.csv'},
        dataflow_default_options={
            'project': project_id,
            'stagingLocation': f'gs://{bucket_path}/df_staging',
            'tempLocation': f'gs://{bucket_path}/df_temp',
            'serviceAccountEmail': f'tf-sa-931@{project_id}.iam.gserviceaccount.com'
        }
    )

    dataflow_template_op = DataflowTemplateOperator(
        task_id='log-review-gcs-csv-to-bq',
        retries=0,
        template=f'gs://{bucket_path}/templates/raw_log_review_gcs_csv_to_bq',
        job_name='gcs-csv-to-bq-log-review',
        parameters={'input': f'gs://{bucket_path}/data/log_review_minimal.csv'},
        dataflow_default_options={
            'project': project_id,
            'stagingLocation': f'gs://{bucket_path}/staging',
            'tempLocation': f'gs://{bucket_path}/temp',
            'serviceAccountEmail': f'tf-sa-931@{project_id}.iam.gserviceaccount.com'
        }
    )
