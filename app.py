from flask import Flask, render_template
from pymongo import MongoClient
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# MongoDB client setup
client = MongoClient("mongodb://localhost:27017/")
db = client.monitoring_app

# Route to render the main HTML page with data
@app.route('/')
def index():
    metrics = list(db.metrics.find({}, {'_id': 0, 'timestamp': 1, 'uptime': 1, 'users_connected': 1, 'activity': 1}))
    notifications = list(db.notifications.find({}, {'_id': 0, 'timestamp': 1, 'event_type': 1, 'description': 1}))

    # Debugging output
    print("Metrics Data:", metrics)
    print("Notifications Data:", notifications)

    # Format timestamps for readability
    for metric in metrics:
        metric['timestamp'] = metric['timestamp'].strftime("%a, %d %b %Y %H:%M:%S GMT")
    for notification in notifications:
        notification['timestamp'] = notification['timestamp'].strftime("%a, %d %b %Y %H:%M:%S GMT")

    return render_template('index.html', metrics=metrics, notifications=notifications)

if __name__ == '__main__':
    app.run(debug=True)
