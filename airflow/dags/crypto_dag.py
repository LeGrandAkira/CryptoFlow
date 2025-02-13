from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
import psycopg2
from minio import Minio
import io
import json

def fetch_and_store_crypto_data():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum",
        "vs_currencies": "usd"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        print("Données récupérées :", data)

        conn = psycopg2.connect(
            dbname="cryptoflow",
            user="airflow",
            password="airflow",
            host="postgres",
            port="5432"
        )
        cursor = conn.cursor()

        for crypto, info in data.items():
            cursor.execute(
                "INSERT INTO crypto_prices (crypto_name, price_usd) VALUES (%s, %s)",
                (crypto, info['usd'])
            )

        conn.commit()
        cursor.close()
        conn.close()
        print("Données insérées dans PostgreSQL.")

        client = Minio(
            "minio:9000",
            access_key="minio",
            secret_key="minio123",
            secure=False
        )

        json_data = json.dumps(data)
        json_bytes = json_data.encode('utf-8')
        json_stream = io.BytesIO(json_bytes)

        client.put_object(
            "crypto-data",
            f"crypto_prices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            json_stream,
            len(json_bytes)
        )
        print("Données uploadées dans MinIO.")

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des données CoinGecko : {e}")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'crypto_data_collection',
    default_args=default_args,
    schedule_interval=timedelta(minutes=60),
) as dag:

    fetch_and_store_task = PythonOperator(
        task_id='fetch_and_store_crypto_data',
        python_callable=fetch_and_store_crypto_data,
    )

    fetch_and_store_task