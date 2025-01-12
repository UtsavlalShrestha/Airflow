# Airflow Weather Data Pipeline

This project implements an Apache Airflow pipeline that retrieves weather data from the [Open Meteo API](https://open-meteo.com/), transforms the data, and loads it into a PostgreSQL database on a daily schedule. The pipeline is orchestrated using Airflow, and the process runs at a daily interval to ensure that the database is continuously updated with the latest weather data.

## Workflow Overview

The pipeline performs the following steps:
1. **Data Extraction**: The Airflow HTTP Hook is used to fetch weather data from the Open Meteo API.
2. **Data Transformation**: The raw data retrieved from the API is processed and transformed to match the required schema for storage.
3. **Data Loading**: The transformed data is then loaded into a PostgreSQL database for further analysis or use.

The pipeline is designed to run daily, ensuring up-to-date weather data is always available in the database.




