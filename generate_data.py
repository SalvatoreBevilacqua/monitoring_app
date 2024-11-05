from pymongo import MongoClient
from faker import Faker
from datetime import datetime, timedelta
import random

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.monitoring_app  # Name of the database
metrics_collection = db.metrics
notifications_collection = db.notifications

# Set up the Faker library to generate random data
fake = Faker()

# Define realistic descriptions for unauthorized access attempts
descriptions = [
    "Suspicious login attempt detected.",
    "Potential unauthorized access flagged by security protocol.",
    "Multiple failed login attempts detected.",
    "Unusual access pattern noticed by system.",
    "Login attempt from an unrecognized device."
]

# Function to generate data for the last 3 months / historical data
def generate_historical_data():
    start_date = datetime.now() - timedelta(days=90)
    current_date = start_date

    while current_date <= datetime.now():
        # Generate uptime and user connection data
        uptime = random.randint(95, 100)  # Simulated uptime percentage
        users_connected = random.randint(1, 50)  # Simulated user count
        activity = "Suspicious" if random.random() < 0.05 else "Normal"  # 5% chance of suspicious activity

        # Insert metrics data into MongoDB
        metrics_data = {
            "timestamp": current_date,
            "uptime": uptime,
            "users_connected": users_connected,
            "activity": activity
        }
        
        try:
            metrics_collection.insert_one(metrics_data)
        except Exception as e:
            print(f"Error inserting metrics data: {e}")

        # Insert a notification if activity is suspicious
        if activity == "Suspicious":
            notification_data = {
                "timestamp": current_date,
                "event_type": "Unauthorized Access Attempt",
                "description": random.choice(descriptions)  # Select a random realistic description
            }
            
            try:
                notifications_collection.insert_one(notification_data)
            except Exception as e:
                print(f"Error inserting notification data: {e}")

        # Move to the next day
        current_date += timedelta(days=1)

    print("Historical data generated successfully!")

if __name__ == "__main__":
    generate_historical_data()
