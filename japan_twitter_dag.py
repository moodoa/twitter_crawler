from airflow import DAG
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator
from airflow.operators.python_operator import PythonOperator

from datetime import datetime, timedelta
from initialize import article_collector

default_args = {
    "owner": "weed",
    "start_date": datetime(2020, 10, 2, 10, 10),
    "retries": 2,
    "retry_delay": timedelta(seconds=5),
}

def article_sender():
    attachments_list = article_collector(access_token,
                        access_token_secret,
                        consumer_key,
                        consumer_secret,
                        accounts,
                        color,
                        min_ago)
    if attachments_list:
        send_notification = SlackWebhookOperator(
            task_id="send_notification",
            webhook_token="YOUR_TOKEN",
            attachments=attachments_list,
            channel='#YOUR_CHANNEL',
        ).execute(context=None)

with DAG(
    "CRAWL_JAPAN_TWITTER",
    default_args=default_args,
    schedule_interval=timedelta(seconds=600),
    catchup=False,
) as dag:
    PythonOperator(python_callable=article_sender, task_id="CRAWL_JAPAN_TWITTER")