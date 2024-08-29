
# Airless

<!-- Pytest Coverage Comment:Begin -->
<!-- Pytest Coverage Comment:End -->

[![PyPI version](https://badge.fury.io/py/airless.svg)](https://badge.fury.io/py/airless)

Airless is a package that aims to build a serverless and lightweight orchestration platform, creating workflows of multiple tasks being executed on [Google Cloud Functions](https://cloud.google.com/functions)


## Why not just use [Apache Airflow](https://airflow.apache.org/)?

Airflow is the industry standard when we talk about job orchestration and worflow management. However, in some cases, we believe it may not be the best solution. I would like to highlight 3 main cases we face that Airflow struggles to handle.

* Serverless

At the beginning of a project we want to avoid dealing with infrastructure since it demands time and it has a fixed cost to reserve an instance to run Airflow. Since we didn't have that many jobs, it didn't make sense to have an instance of Airflow up 24-7. 

When the project starts to get bigger and, if we use Airflow's instance to run the tasks, we start facing performance issues on the workflow.

In order to avoid this problems we decided to build a 100% serverless platform.

* Parallel processing

The main use case we designed Airless for is for data scrappers. The problem with data scrappers is that normally you want them to process a lot of tasks in parallel, for instance, first you want to fetch a website and collect all links in that page and send them forward for another task to be executed and then that task does the same and so on and so forth.

Building this workflow that does not know before hand how many tasks are going to be executed is something hard be built on Airflow.

* Data sharing between tasks

In order to built this massive parallel processing workflow that we explained on the previous topic, we need to be able to dynamically create and send data to the next task. So use the data from the first task as a trigger and an input data for the next tasks. 

## How it works

Airless builts its workflows based on [Google Cloud Functions](https://cloud.google.com/functions), [Google Pub/Sub](https://cloud.google.com/pubsub) and [Google Cloud Scheduler](https://cloud.google.com/scheduler).

1. Everything starts with the Cloud Scheduler, which is a serverless product from Google Cloud that is able to publish a message to a Pub/Sub with a cron scheduler
2. When a message is published to a Pub/Sub it can trigger a Cloud Function and get executed with that message as an input
3. This Cloud Functions is able to publish as many messages as it wants to as many Pub/Sub topics as it wants
4. Repeat from 2


## Preparation

### Environment variables

* `ENV`
* `GCP_PROJECT`
* `PUBSUB_TOPIC_ERROR`
* `LOG_LEVEL`
* `PUBSUB_TOPIC_EMAIL_SEND`
* `PUBSUB_TOPIC_SLACK_SEND`
* `BIGQUERY_DATASET_ERROR`
* `BIGQUERY_TABLE_ERROR`
* `EMAIL_SENDER_ERROR`
* `EMAIL_RECIPIENTS_ERROR`
* `SLACK_CHANNELS_ERROR`