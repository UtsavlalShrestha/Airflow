from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from airflow.utils.dates import days_ago
from datetime import timedelta
import requests, json


Latitude = '27.6999'
Longitude = '85.0004'
Postgres_conn_id = 'postgres_default'
Api_conn_id = 'open_meteo_api'

with DAG(
    dag_id = 'etl_eather_pipeline',
    default_args={
        'owner': 'airflow',
        'start_date': days_ago(1),
        # 'retries': 1,
        # 'retry_delay': timedelta(seconds=5),
        },
        schedule_interval='0 0 * * *',
        catchup= False
)as dags:
    @task()
    def get_weather_data():
        # extracting weather data from open meteo api

        # httphook to get connection details
        http_hook = HttpHook(http_conn_id = Api_conn_id, method = 'GET')

        # Build the API endpoint
        # https://api.open-meteo.com/v1/forecast?latitude=51.5074&longitude=-0.1278&current_weather=true
        endpoint=f'/v1/forecast?latitude={Latitude}&longitude={Longitude}&current_weather=true'

        #making request via http_hook
        response = http_hook.run(endpoint)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Feetching failure: {response.status_code}")
    
    @task()
    def transform_eather_data(weather_data):
        curr_weather = weather_data['current_weather']
        elevation = weather_data['elevation']
        transformed_data = {
            'latitude': Latitude,
            'longitude': Longitude,
            'elevation': elevation,
            'temperature': curr_weather['temperature'],
            'windspeed': curr_weather['windspeed'],
            'winddirection': curr_weather['winddirection'],
            'weathercode': curr_weather['weathercode']
        }
        return transformed_data

    @task()
    def load_transformed_data(transformed_data):
        #loading data into Postgres
        pg_hook = PostgresHook(postgres_conn_id = Postgres_conn_id)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()    

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_data(
                latitude FLOAT,
                longitude FLOAT,
                elevation FLOAT,
                temperature FLOAT,
                windspeed FLOAT,
                winddirection FLOAT,
                weathercode INT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            """)
        
        cursor.execute("""
            INSERT INTO weather_data(latitude, longitude, elevation,temperature, windspeed, winddirection, weathercode)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                transformed_data['latitude'],
                transformed_data['longitude'],
                transformed_data['elevation'],
                transformed_data['temperature'],
                transformed_data['windspeed'],
                transformed_data['winddirection'],
                transformed_data['weathercode']
            ))
            
        conn.commit()
        cursor.close()

    weather_data= get_weather_data()
    transformed_data = transform_eather_data(weather_data)
    load_transformed_data(transformed_data)

    #dependency description not needed as decorator handles it sequentially as mentioned, if diff sequeencce then can use bitwise operator
    #get_weather_data() >> transform_eather_data(weather_data) >> load_transformed_data(transformed_data)
    


        
        