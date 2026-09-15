# Dockerized Real-Time CDC Data Pipeline with PostgreSQL, Kafka, and Hadoop

## Overview

This project implements an enterprise-grade real-time Change Data Capture (CDC) pipeline for streaming transactional data from PostgreSQL into a big data environment using Debezium, Apache Kafka, Hadoop/HDFS, Hive, and Apache Airflow.

The objective of this project is to demonstrate how database changes such as inserts, updates, and deletes can be captured automatically, streamed reliably, stored in distributed systems, and orchestrated through automated workflows for downstream analytics and monitoring.

This project was designed as a practical data engineering solution that simulates a real-world production pipeline architecture.

---

## Project Objectives

- Capture real-time changes from a PostgreSQL database using CDC
- Stream database events through Apache Kafka using Debezium
- Store streamed data into a Hadoop ecosystem for scalable processing
- Enable querying and analytics through Hive
- Automate pipeline execution and validation using Apache Airflow

---

## Architecture

The pipeline follows this flow:

**PostgreSQL → Debezium → Kafka → Sink Consumer / Hadoop-Hive → Airflow Orchestration**

### Main Components

- **PostgreSQL**: Source relational database containing transactional records
- **Debezium**: Captures row-level changes from PostgreSQL and publishes them to Kafka topics
- **Apache Kafka**: Message broker for transporting CDC events in real time
- **Kafka Connect**: Connects source and sink systems
- **Hadoop / HDFS**: Distributed storage layer for persisting streamed data
- **Hive**: Query engine for structured analytics on ingested data
- **Apache Airflow**: Workflow orchestration for automation and scheduling
- **Python Test Generator**: Automatically inserts, updates, and deletes records for testing CDC behavior

---

## Key Features

- Real-time CDC from PostgreSQL using Debezium
- Kafka-based streaming architecture
- Automatic propagation of insert, update, and delete events
- Data persistence into Hadoop/HDFS
- Query-ready storage with Hive integration
- Workflow orchestration with Airflow DAGs
- Automatic test data generation for validation
- Containerized deployment with Docker Compose
- Modular service separation for enterprise-style architecture
- Data quality checks and pipeline monitoring

---

## Tech Stack
0
### Programming / Automation
- Python
- SQL
- Docker
- Docker Compose

### Monitoring / Validation
- Logs inspection
- Sink file validation
- Event flow testing
- CDC operation verification

---

## Use Case

This project simulates a real-world business environment where transactional data changes continuously and must be captured, transferred, and stored without manual intervention.

Typical use cases include:
- customer order tracking
- inventory change monitoring
- operational event streaming
- real-time analytics pipelines
- audit-ready data movement across systems

---

## Dataset / Table Schema

The sample PostgreSQL table includes fields such as:

- `customer_name`
- `product`
- `quantity`
- `order_status`

These fields are used to simulate transactional operations and validate CDC event propagation across the pipeline.

---

## Project Structure

```bash
real-time-cdc-data-pipeline/
│
├── airflow/
│   ├── dags/
│   │   └── pipeline_orchestration_dag.py
│   └── config/
│
├── connectors/
│   ├── debezium-postgres-connector.json
│   └── sink-connector.json
│
├── postgres/
│   ├── init.sql
│   └── sample_data.sql
│
├── scripts/
│   ├── test_generator.py
│   ├── data_validation.py
│   └── monitor_pipeline.py
│
├── hive/
│   └── hive_setup.sql
│
├── docker-compose.yml
├── requirements.txt
├── README.md
└── screenshots/
