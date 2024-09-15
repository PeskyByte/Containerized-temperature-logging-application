import mysql.connector
import pymongo
import time
from mysql.connector.errors import DatabaseError


def get_db_connection(max_retries=5, delay=5):
    for attempt in range(max_retries):
        try:
            connection = mysql.connector.connect(
                host='db',
                user='root',
                password='rootpassword',
                database='tempdb'
            )
            return connection
        except DatabaseError as e:
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                raise

def get_mongo_connection():
    client = pymongo.MongoClient("mongodb://mongo:27017/")
    return client.analytics_db

def calculate_analytics():
    mysql_conn = get_db_connection()
    cursor = mysql_conn.cursor()
    
    cursor.execute("SELECT MIN(reading), MAX(reading), AVG(reading) FROM temperature_readings")
    min_temp, max_temp, avg_temp = cursor.fetchone()
    
    cursor.close()
    mysql_conn.close()
    
    
    return {
        "min_temperature": min_temp,
        "max_temperature": max_temp,
        "avg_temperature": avg_temp,
        "timestamp": time.time()
    }

def store_analytics(analytics):
    mongo_db = get_mongo_connection()
    result = mongo_db.temperature_analytics.insert_one(analytics)

if __name__ == "__main__":
    while True:
        try:
            analytics = calculate_analytics()
            store_analytics(analytics)
        except Exception as e:
            pass
        time.sleep(10)