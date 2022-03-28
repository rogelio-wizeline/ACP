import datetime

from airflow import models
from airflow.providers.google.cloud.operators.dataflow import \
    DataflowTemplatedJobStartOperator
from airflow.contrib.operators.dataflow_operator import DataflowTemplateOperator
from airflow.utils.dates import days_ago

bucket_path = "rg-acp-storage"
project_id = "shaped-icon-344520"
gce_zone = "us-central1-a"


default_args = {
    "start_date": days_ago(1),
    "dataflow_default_options": {
        "project": project_id,
        "zone": gce_zone,
        "tempLocation": f"gs://{bucket_path}/tmp/"
    },
}

with models.DAG(
    "transactional_layer",
    default_args=default_args,
    schedule_interval=None,
) as dag:
    dataflow_template_op = DataflowTemplateOperator(
        task_id='transactional-layer-dag',
        retries=0,
        template='gs://rg-acp-storage/templates/transactional_purchase_gcs_csv_to_bq',
        job_name='transactional_layer',
        parameters={'input': 'gs://rg-acp-storage/data/purchase_minimal.csv'},
        dataflow_default_options={
            "project": "shaped-icon-344520",
            "stagingLocation": "gs://rg-acp-storage/staging",
            "tempLocation": "gs://rg-acp-storage/temp",
            "serviceAccountEmail": "tf-sa-931@shaped-icon-344520.iam.gserviceaccount.com"
        }
    )

