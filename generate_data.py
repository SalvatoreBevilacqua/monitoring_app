from pymongo import MongoClient
from faker import Faker
from datetime import datetime, timedelta
import random

# Connect to MongoDB (adjust the URI if you're using MongoDB Atlas or another connection)
client = MongoClient("mongodb://localhost:27017/")
db = client.monitoring_app  # Name of the database
metrics_collection = db.metrics
notifications_collection = db.notifications

# Set up the Faker library to generate random data
fake = Faker()

# Function to generate data for the last 3 months
def generate_historical_data():
    start_date = datetime.now() - timedelta(days=90)
    current_date = start_date

    while current_date <= datetime.now():
        # Generate uptime and user connection data
        uptime = random.randint(95, 100)  # Simulated uptime percentage
        users_connected = random.randint(1, 50)  # Simulated user count
        activity = "Suspicious" if random.random() < 0.05 else "Normal"  # 5% chance of suspicious activity

        # Insert metrics data into MongoDB
        metrics_collection.insert_one({
            "timestamp": current_date,
            "uptime": uptime,
            "users_connected": users_connected,
            "activity": activity
        })

        # Insert a notification if activity is suspicious
        if activity == "Suspicious":
            notifications_collection.insert_one({
                "timestamp": current_date,
                "event_type": "Unauthorized Access Attempt",
                "description": fake.sentence()
            })

        # Move to the next day
        current_date += timedelta(days=1)

    print("Historical data generated successfully!")

if __name__ == "__main__":
    generate_historical_data()
