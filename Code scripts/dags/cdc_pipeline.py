from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

with DAG(
    dag_id="cdc_pipeline",
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
) as dag:
    # Entry point
    start = DummyOperator(task_id="Start_Docker")

    # service startup
    start_services = BashOperator(
        task_id="Run_Services",
        bash_command="echo '🚀 Bringing up PostgreSQL, Zookeeper, Kafka, Connect, HDFS and File Sink'"
    )

    # test-data generation
    run_tests = BashOperator(
        task_id="Test_generator",
        bash_command="echo '🔄 Generating and capturing CDC events...'"
    )
    
    # Model CDC flow
    postgres_to_debezium = DummyOperator(task_id="postgres_to_debezium")
    debezium_to_kafka = DummyOperator(task_id="debezium_to_kafka_brokers")
    kafka_topic = DummyOperator(task_id="kafka_topic_stream")
    kafka_connect_to_hdfs = DummyOperator(task_id="kafka_connect_to_hdfs")
    hdfs_sink = DummyOperator(task_id="hdfs_sink")
    file_sink = DummyOperator(task_id="file_sink")


    # airflow post-processing
    airflow_post = DummyOperator(task_id="airflow_post_processing")


    # Define linear fake execution graph
    start >> start_services >> postgres_to_debezium  >> run_tests >> debezium_to_kafka >> kafka_topic \
         >> kafka_connect_to_hdfs >> hdfs_sink >> file_sink \
         >> airflow_post 
