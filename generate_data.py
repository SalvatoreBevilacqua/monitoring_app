from pymongo import MongoClient
from datetime import datetime, timedelta
import random

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.monitoring_app
metrics_collection = db.metrics
notifications_collection = db.notifications

# Semplici descrizioni senza Faker
descriptions = [
    "Suspicious login attempt detected.",
    "Potential unauthorized access flagged.",
    "Multiple failed login attempts detected.",
    "Unusual access pattern noticed.",
    "Login attempt from unrecognized device."
]

def generate_data(days=90):
    start_date = datetime.now() - timedelta(days=days)
    current_date = start_date
    
    print(f"Generating {days} days of data...")
    metrics_count = 0
    notifications_count = 0

    while current_date <= datetime.now():
        # Generate simplified random data
        uptime = random.uniform(90.0, 100.0)
        uptime = round(uptime, 2)
        users = random.randint(5, 50)
        activity = "Suspicious" if random.random() < 0.1 else "Normal"
        
        # Create timestamp with random time
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        timestamp = current_date.replace(hour=hour, minute=minute)
        
        # Insert metrics
        metrics_data = {
            "timestamp": timestamp,
            "uptime": uptime,
            "users_connected": users,
            "activity": activity
        }
        
        metrics_collection.insert_one(metrics_data)
        metrics_count += 1
        
        # Create notification if suspicious
        if activity == "Suspicious":
            notification_data = {
                "timestamp": timestamp,
                "event_type": "Unauthorized Access Attempt",
                "description": random.choice(descriptions)
            }
            notifications_collection.insert_one(notification_data)
            notifications_count += 1
            
        current_date += timedelta(days=1)
    
    print(f"Successfully generated {metrics_count} metrics and {notifications_count} notifications")

if __name__ == "__main__":
    # Clear existing data
    metrics_collection.delete_many({})
    notifications_collection.delete_many({})
    print("Collections cleared")
    
    # Generate new data
    generate_data(90)