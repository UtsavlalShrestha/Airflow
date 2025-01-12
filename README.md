# Airflow Weather Data Pipeline

This project implements an Apache Airflow pipeline that retrieves weather data from the [Open Meteo API](https://open-meteo.com/), transforms the data, and loads it into a PostgreSQL database on a daily schedule. The pipeline is orchestrated using Airflow, and the process runs at a daily interval to ensure that the database is continuously updated with the latest weather data.

## Workflow Overview

The pipeline performs the following steps:
1. **Data Extraction**: The Airflow HTTP Hook is used to fetch weather data from the Open Meteo API.
2. **Data Transformation**: The raw data retrieved from the API is processed and transformed to match the required schema for storage.
3. **Data Loading**: The transformed data is then loaded into a PostgreSQL database for further analysis or use.

The pipeline is designed to run daily, ensuring up-to-date weather data is always available in the database.

## Features
- **ETL Process**: Extract, transform, and load (ETL) weather data into PostgreSQL.
- **Scheduled Runs**: The pipeline runs daily using Airflow's scheduling capabilities.
- **HTTP Hook**: Utilizes Airflow’s HTTP hook to interact with the Open Meteo API.
- **PostgreSQL Database**: Stores the processed data into a PostgreSQL database for easy access and querying.

## Prerequisites

Before running the pipeline, ensure that you have the following set up:
- **Apache Airflow**: The project is built on Apache Airflow. Install Airflow if you haven't already.
- **PostgreSQL**: A PostgreSQL database where the transformed weather data will be stored.
- **Python Dependencies**: The project requires several Python libraries. You can install them using the provided `requirements.txt` file.

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/airflow-weather-pipeline.git
   cd airflow-weather-pipeline
