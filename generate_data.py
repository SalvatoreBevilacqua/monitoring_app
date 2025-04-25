from pymongo import MongoClient
from faker import Faker
from datetime import datetime, timedelta
import random
import argparse
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Set up command line arguments
parser = argparse.ArgumentParser(description='Generate test data for the monitoring app')
parser.add_argument('--days', type=int, default=90, help='Number of days of historical data to generate')
parser.add_argument('--reset', action='store_true', help='Reset collections before generating new data')
parser.add_argument('--connection', type=str, default=None, help='MongoDB connection string')
args = parser.parse_args()

# MongoDB connection
MONGO_URI = args.connection or os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "monitoring_app")

# Connect to MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]  # Name of the database
    
    # Test connection
    client.admin.command('ping')
    logger.info(f"Successfully connected to MongoDB at {MONGO_URI}")
    
    metrics_collection = db.metrics
    notifications_collection = db.notifications
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    raise

# Set up the Faker library to generate random data
fake = Faker()

# Define realistic event types
event_types = [
    "Unauthorized Access Attempt",
    "System Resource Warning",
    "Service Restart",
    "Configuration Change",
    "Database Backup"
]

# Define realistic descriptions for different event types
descriptions_by_type = {
    "Unauthorized Access Attempt": [
        "Suspicious login attempt detected from IP {ip}.",
        "Multiple failed login attempts for user {user}.",
        "Potential brute force attack detected.",
        "Unusual access pattern from {location}.",
        "Login attempt from unrecognized device."
    ],
    "System Resource Warning": [
        "CPU usage exceeded 90% for over 5 minutes.",
        "Memory usage critically high (95%).",
        "Disk space below 10% on main storage.",
        "Network bandwidth saturation detected.",
        "Database connection pool nearly exhausted."
    ],
    "Service Restart": [
        "Service {service} restarted automatically.",
        "Scheduled maintenance restart completed.",
        "Emergency restart triggered by monitoring system.",
        "Service restarted after crash.",
        "Rolling update restart completed successfully."
    ],
    "Configuration Change": [
        "Security settings updated by admin.",
        "Firewall rules modified.",
        "Database configuration optimized.",
        "Load balancer settings adjusted.",
        "API rate limits reconfigured."
    ],
    "Database Backup": [
        "Scheduled backup completed successfully.",
        "Incremental backup finished in {time} minutes.",
        "Backup verification passed all checks.",
        "Cloud backup synchronized.",
        "Database backup size: {size}GB."
    ]
}

# Function to generate a realistic description
def generate_description(event_type):
    templates = descriptions_by_type.get(event_type, ["Generic event occurred."])
    template = random.choice(templates)
    
    # Fill in any template variables
    if "{ip}" in template:
        template = template.replace("{ip}", fake.ipv4())
    if "{user}" in template:
        template = template.replace("{user}", fake.user_name())
    if "{location}" in template:
        template = template.replace("{location}", fake.country())
    if "{service}" in template:
        template = template.replace("{service}", random.choice(["nginx", "mongodb", "application-server", "api-gateway", "cache-service"]))
    if "{time}" in template:
        template = template.replace("{time}", str(random.randint(3, 45)))
    if "{size}" in template:
        template = template.replace("{size}", str(random.randint(1, 50)))
        
    return template

# Reset collections if requested
if args.reset:
    try:
        metrics_collection.delete_many({})
        notifications_collection.delete_many({})
        logger.info("Collections reset successfully")
    except Exception as e:
        logger.error(f"Error resetting collections: {e}")

# Function to generate data for the specified number of days
def generate_historical_data(days=90):
    start_date = datetime.now() - timedelta(days=days)
    current_date = start_date
    metrics_count = 0
    notifications_count = 0

    logger.info(f"Generating {days} days of historical data starting from {start_date.strftime('%Y-%m-%d')}")

    while current_date <= datetime.now():
        # Add some randomness to the timestamp within the day
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        current_datetime = current_date.replace(hour=hour, minute=minute, second=second)
        
        # Generate uptime with occasional dips
        is_problematic_day = random.random() < 0.05  # 5% chance of a problematic day
        
        if is_problematic_day:
            uptime = random.uniform(85.0, 94.9)  # Lower uptime on problematic days
        else:
            uptime = random.uniform(98.0, 100.0)  # Normal uptime
            
        uptime = round(uptime, 2)  # Round to 2 decimal places
        
        # Generate user connection data with day/night patterns
        if 8 <= hour <= 20:  # Working hours
            users_connected = random.randint(20, 50)  # More users during the day
        else:
            users_connected = random.randint(5, 20)  # Fewer users at night
            
        # Add some weekly patterns (more users on weekdays)
        if current_date.weekday() < 5:  # Monday to Friday
            users_connected = int(users_connected * 1.2)
        
        # Determine activity status
        if uptime < 95 or random.random() < 0.08:  # Problematic uptime or random chance
            activity = "Suspicious"
        else:
            activity = "Normal"

        # Insert metrics data into MongoDB
        metrics_data = {
            "timestamp": current_datetime,
            "uptime": uptime,
            "users_connected": users_connected,
            "activity": activity
        }
        
        try:
            metrics_collection.insert_one(metrics_data)
            metrics_count += 1
        except Exception as e:
            logger.error(f"Error inserting metrics data: {e}")

        # Insert a notification if activity is suspicious
        if activity == "Suspicious":
            event_type = "Unauthorized Access Attempt"
            notification_data = {
                "timestamp": current_datetime,
                "event_type": event_type,
                "description": generate_description(event_type)
            }
            
            try:
                notifications_collection.insert_one(notification_data)
                notifications_count += 1
            except Exception as e:
                logger.error(f"Error inserting notification data: {e}")
                
        # Add some random system events (not just based on suspicious activity)
        if random.random() < 0.15:  # 15% chance each day to have other types of events
            # Random event that's not an unauthorized access attempt
            other_event_types = [et for et in event_types if et != "Unauthorized Access Attempt"]
            event_type = random.choice(other_event_types)
            
            # Create event at a different time in the day
            event_hour = (hour + random.randint(1, 6)) % 24
            event_minute = random.randint(0, 59)
            event_datetime = current_date.replace(hour=event_hour, minute=event_minute, second=random.randint(0, 59))
            
            notification_data = {
                "timestamp": event_datetime,
                "event_type": event_type,
                "description": generate_description(event_type)
            }
            
            try:
                notifications_collection.insert_one(notification_data)
                notifications_count += 1
            except Exception as e:
                logger.error(f"Error inserting additional notification data: {e}")

        # Move to the next day
        current_date += timedelta(days=1)

    logger.info(f"Historical data generation completed: {metrics_count} metrics and {notifications_count} notifications created")
    return metrics_count, notifications_count

if __name__ == "__main__":
    metrics_count, notifications_count = generate_historical_data(args.days)
    print(f"Successfully generated {metrics_count} metrics and {notifications_count} notifications")