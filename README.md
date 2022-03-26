# Wizeline Academy Data Engineering Apprenticeship

This repository was made for the DE Apprenticeship capstone project.
It's divided into seven milestones.

The course content is described as follows, but several modifications were made on the run, and are described after each milestone's intent explanation (after a dashed line).

This project assumes that you have a file named `terraform.tfvars` at the root of the project with the following:
```terraform
project_id = <YOUR_GCP_PROJECT_ID>
region = <YOUR_REGION>
zone = <YOUR_ZONE>
```

## Milestone 1

##### TODO:
- Take as reference Terraform reference, identify and select the corresponding terraform blocks to build your own Airflow Cluster.
- Airflow Cluster must be built with GKS in Google or EKS in AWS.
- In case of some difficulties, take advantage of templates provided by Wizeline to build and start your Airflow Cluster.
- Take your notes about any blocker and your lessons learned to be discussed during Q&A and Mentoring sessions.

##### OUTCOME:
- Terraform blocks to build and run your Airflow Cluster.
- (Optional) Automation process to run Terraform blocks as part of the
main Data Pipeline.

##### NOTES:
- Take as a reference the video from the meeting “[DE Apprenticeship] Study Group - Grisell/Marco" attached to this section to watch step by step the implementation on GCP and AWS. Disclaimer:the video is only in Spanish by now.
- What has been listed in this milestone is just for guidance and to help you distribute your workload; you can build more or fewer items if necessary. However, if you build fewer items at this point, you have to cover the remaining tasks in the next milestone.
- Do not hesitate to ask for mentoring if you need help with this exercise, remember that you can do it by our Slack channel "dataeng-apprenticeship".

---
##### Solution and modifications
To solve this milestone, I just used Google Cloud Composer with all the default settings. DAGs can be found in the `dags` folder.

## Milestone 2
On the drive folder you will find two resources for this milestone:
- A png file with the schema to create your user_purchase table.
- The user_purchase.csv file.

Based on the self-study material, recorded and live session, and mentorship covered until this deliverable, we suggest you perform the following:

##### TODO:
- Use your up and running Airflow Cluster to create your DAGs.
- Think about the best way to design your data pipeline. Remember to include new concepts you were learning in previous weeks.
- Use terraform blocks to set up your environment, you will need to create a new PostgreSQL DB with one table named user_purchase.
(PostgreSQL_Table_Schema.png)
- Use Airflow to upload the user_purchase.csv file into the new PostgreSQL table. Remember there's more than one way to complete this step.

##### OUTCOME:
- PostgreSQL table named user_purchase.
- Airflow job to load user_purchase.csv in user_purchase table.
- Terraform blocks to create PostgreSQL DB and table. Also, IAM needed to integrate Airflow Cluster and SQL service.
- (Optional) Automation process to run Terraform blocks as part of the main Data Pipeline

##### NOTES:
- What has been listed in this milestone is just for guidance and to help you distribute your  workload; you can build more or fewer items if necessary. However, if you build fewer items at this point, you have to cover the remaining tasks in the next milestone.
- Do not hesitate to ask for mentoring if you need help with this exercise, remember that you can do it by our Slack channel "dataeng-apprenticeship".

---
##### Solution and modifications:

For this milestone, I made an `Apache Beam` file to run in `Dataflow`. It's intended to be used as a template on `Dataflow`.
I also changed PostgreSQL in Cloud SQL for BigQuery, as it's *way* easier to work with BQ in Dataflow. BigQuery has a dataset called `transactional` where I create a table `user_reviews` with the info from the CSV file.

###### Creating a template

A template needs to be uploaded as an encoded JSON file. To do that, you can run the dataflow job in your machine as you would run a regular job, but adding the `--template_location=gs://<BUCKET>/path/to/template/folder/<TEMPLATE_NAME>` parameter when running it. The template name is best left without file extension. For example:

```
python dataflow/test_template.py  --template_location=gs://<BUCKET>/templates/test_template
```

Keep in mind you need to have apache-beam installed. This project was developed using Python3.9 and apache-beam 2.37.0.

To develop an apache beam job to be run in Dataflow as a template, the process is pretty much the same as a regular job, but any parameters that will be used in you job need to go through `ValueProvider`. `ValueProvider` values can __only__ be used as parameters for ParDo/DoFn functions (that's seldom advertised in the docs).

After running the command above, a file named `test_template` will be created.

To accept parameters, you'll need a `metadata` file. It's a JSON file that contains certain data the template will use... this is evident when you use the Dataflow UI. For it to work, it needs to be named like: <TEMPLATE_NAME>_metadata. If your template is called `test_template`, then the metadata file __must__ be named `test_template_metadata`, without any extension.

Note that if you named your template with an extension, for example `test_template.json`, the metadata file __must__ be named `test_template.json_metadata`. It's an awkward naming, so it's best to leave your template file without any extension.

A metadata file looks like this:
```
{
  "name": "Test1",
  "description": "An example pipeline that prints the parameter received.",
  "parameters": [
    {
      "name": "to_print",
      "label": "String to print",
      "helpText": "String to print in the pipeline's console."
    }
  ]
}
```

More about metadata can be found [here](https://cloud.google.com/dataflow/docs/guides/templates/creating-templates#using-metadata-in-your-pipeline-code).

After you've created your metadata file, it needs to be placed in the same folder as your template file in GCS. In our example we placed our template in `gs://<BUCKET>/path/to/template/folder/<TEMPLATE_NAME>`, so our file must be in `gs://<BUCKET>/path/to/template/folder/<TEMPLATE_NAME>_metadata`.

###### Running the template:
A dataflow template can be run from the `Dataflow UI`, with the `gcloud` CLI, with `REST`, or with `DataflowTemplatedJobStartOperator` in Airflow. We'll do the latter for the project, but for testing purposes, using the Dataflow UI works wonders.

To run in Airflow, you'll need something like this in your DAG:
```
start_template_job = DataflowTemplatedJobStartOperator(
    task_id="start-template-job",
    template='gs://<BUCKET>/templates/test_template',
    parameters={'to_print': 'holi desde airflow'},
    location='us-central1'
)
```

## Milestone 3
On the drive folder you will find two resources for this milestone:
- movie_review.csv file
- log_reviews.csv file

Based on the self-study material, recorded and live session, and mentorship covered until this deliverable, we suggest you perform the following:

##### TODO:
- Use your up and running Airflow Cluster to create your DAGs.
- Think about the best way to design your data pipeline. Remember to include new concepts you are learning in previous weeks.
- Use terraform blocks to set up your environment, you will need to create storage resources. S3 for AWS and Cloud Storage for GCP. One bucket for your Raw Layer and the other for your Staging Layer.
- Upload movie_review.csv and log_reviews.csv files in your Raw Layer.
- Now it is time to process your data. You have the opportunity to work in a self-managed service such as EMR cluster as follow:
-- Use terraform blocks to create your EMR cluster.
-- Read your PostgreSQL table and write the data in your Staging Layer.
-- Read movie_review.csv from your Raw Layer and write the result in your Staging Layer following the logic listed below. (`Movie review logic`).
-- Read log_reviews.csv from your Raw Layer and write the result in your Staging Layer following the logic listed below. (`Log reviews logic`).
- Another way to process your data is by running serverless services such as Glue in AWS and Dataflow in GCP.
-- Figure out how to work with fully-managed services + Airflow + Terraform.
-- Read your PostgreSQL table and write the data in your Staging Layer.
-- Read movie_review.csv from your Raw Layer and write the result in your Staging Layer following the logic listed below. (`Movie review logic`).
-- Read log_reviews.csv from your Raw Layer and write the result in your Staging Layer following the logic listed below. (`Log reviews logic`).


__Movie review logic:__
- From the movie_review.csv file, work with the cid and review_str columns to get a list of words used by users.
-- Note: You can implement the pyspark.ml.feature.Tokenizer class to create a list of words named review_token.
- Remove stop words if needed with pyspark.ml.feature.StopWordsRemover.
- Look for data that contain the word “good”, consider the review as positive, and name it as positive_review.
- Select the appropriate file format for the next steps.
- Use the following logic to convert positive_review from a boolean to an integer: 

```
reviews.positive_review = CASE
WHEN positive_review IS True THEN 1
ELSE 0 END
```

- Save the data in your STAGE area. What you need is user_id, positive_review, review_id.

__Log reviews logic:__
- From the log_reviews.csv file, map the structure for the DataFrame schema according to the log_review column that contains the xml as a string.
- Work with the log column to get all the metadata and build the columns for your DataFrame.
-- Note: You can use the databricks.spark.xml library
- Don’t forget to drop the log column by the end.
- Store your results into a new file in the STAGE area (log_id, log_date device, os, location, browser, ip, phone_number).

##### OUTCOME:
- Classified movie reviews in Staging Layer named movie_reviews.
- Classified log reviews in Staging Layer named log_reviews
- PostgreSQL exported data to Staging Layer named user_purchase
- Terraform blocks to create Raw and Staging, create and run distributed environment (e.g. EMR). Also, IAM needed to integrate Airflow Cluster with the rest of the cloud services used in your Data Pipeline.
- Code where you run the `Movie review Logic` & `Log reviews logic` in a distributed manner.

##### NOTES:
- What has been listed in this milestone is just for guidance and to help you distribute your workload; you can build more or fewer items if necessary. However, if you build fewer items at this point, you have to cover the remaining tasks in the next deliverable.
- Do not hesitate to ask for mentoring if you need help with this exercise, remember that you can do it by our Slack channel "dataeng-apprenticeship".


## Milestone 4

Based on the self-study material, video sessions and mentorship sessions, it is time to work on your Capstone Project. Keep in mind that this milestone will be built with the content of 3 weeks (You are in the 2nd out of 3 weeks).
On the drive folder you will find two resources for this milestone:
- movie_review.csv file
- log_reviews.csv file

For more details read the chapter "Third advance: First step of the ETL implementation" on Module Distributed Work.

##### NOTES:
- What has been listed in this milestone is just for guidance and to help you distribute your workload
- Do not hesitate to ask for mentoring if you need help with this exercise, remember that you can do it by our Slack channel "dataeng-apprenticeship".


## Milestone 5

Based on the self-study material, video sessions and mentorship sessions, it is time to work on your Capstone Project. Keep in mind that this milestone will be built with the content of 3 weeks (You are in the 3rd out of 3 weeks).
On the drive folder you will find two resources for this milestone:
- movie_review.csv file
- log_reviews.csv file
For more details read the chapter "Third advance: First step of the ETL implementation" on Module Distributed Work.

##### NOTES:
- What has been listed in this milestone is just for guidance and to help you distribute your workload
- Do not hesitate to ask for mentoring if you need help with this exercise, remember that you can do it by our Slack channel "dataeng-apprenticeship".


## Milestone 6

Based on the self-study material, video sessions and mentorship sessions, it is time to work on your Capstone Project. We suggest you perform the following.

##### TODO:
- Use your up and running Airflow Cluster to create your DAGs.
- Think about the best way to design your data pipeline. Remember to include new concepts you are learning in previous weeks.
- Use terraform blocks to set up your Data Warehouse. Redshift in AWS and BigQuery in GCP.
- The goal is to run analytics from data stored in your cloud buckets (Staging Layer). For Redshift, you will need to configure Redshift Spectrum, and from BigQuery you will need to configure External Tables.
- Add your IAM policies accordingly to connect your cloud services.
- Create a table in your Data Warehouse, using the schema attached (DW_Table.png)
- Remember to use terraform as much as possible.
- Use your EMR / Glue / Dataflow service to build you dim tables and calculate fact_movie_analytics (Fact movie analytics logic).
- Feel free to run SQL Queries in your new DW table. Fact movie analytics logic:
- Data exported from PostgreSQL and stored in your Staging Layer will be named user_purchase.
- Remember that you stored in the silver zone (STAGING area) the data from movie_review.csv and log_reviews.csv. You have to build 5 dim tables with the next dimensions: date, devices, location, os, browser then build your fact table fact_movie_analytics.
- Classification data calculated from movie_review.csv and now stored in your Staging Layer will be named review.
- Part of the Data Warehouse will be populated following the logic below, complete the missing fields in order to have you DW done:

```
customerid => user_purchase.customerid
amount_spent => SUM(user_purchase.quantity * user_purchase.unit_price)
review_score => SUM(reviews.positive_review)
review_count => COUNT(reviews.id)
insert_date => airflow timestamp
```

Next you will find some of the many metrics that you can build from your data:
- How many reviews were done in California, NY and Texas?
- How many reviews were done in California, NY, and Texas with an apple device? And how many for each device type?
- Which location has more reviews from a computer in a Chrome browser?
- What are the states with more and fewer reviews in 2021?
- Which device is the most used to write reviews in the east and which one in the west?

##### OUTCOME:
- Terraform blocks to create your DW environment and the ability to run external queries. Also, IAM needed to integrate Airflow Cluster and Analytic tasks.
- Code where you run the Fact movie analytics logic in a distributed manner.
- (Optional) Automation process to run Terraform blocks as part of the main Data Pipeline

##### NOTES:
- Do not hesitate to ask for mentoring if you need help with this exercise, remember that you can do it by our Slack channel "dataeng-apprenticeship".


## Milestone 7
You have completed the Capstone project, now you should do the following.

##### TODO:
- Create a report where you will describe the design of your Data Pipeline.
- The expected format is a PPT file which will be used during the demo meeting with Wizeline people.
- Prepare for a tech discussion in terms of:
-- Use of Terraform
-- Data pipeline design
-- Best practices
-- Blockers
-- Lesson learned

__OPTIONAL CHANGES:__
- These changes are not required to be part of your demo but if you are interested in practicing your streaming skills.
- Think about how you would consume movie review data using streaming.

##### OUTCOME:
- PPT file which will be presented during the demo meeting.
