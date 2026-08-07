import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

def connect_to_db():
    try:
        # Establish a connection to the PostgreSQL database
        connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        print("Connection to the database was successful.")
        return connection
    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")
        return None