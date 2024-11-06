from flask import Flask, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# MongoDB client setup
client = MongoClient("mongodb://localhost:27017/")
db = client.monitoring_app

# Route to render the main HTML page
@app.route('/')
def index():
    return render_template('index.html')

# API route for metrics data
@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    metrics = list(db.metrics.find({}, {'_id': 0}))
    # Ensure timestamps are formatted properly
    for metric in metrics:
        metric['timestamp'] = metric['timestamp'].strftime("%a, %d %b %Y %H:%M:%S GMT")
    return jsonify(metrics)

# API route for notifications data
@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    notifications = list(db.notifications.find({}, {'_id': 0}))
    # Ensure timestamps are formatted properly
    for notification in notifications:
        notification['timestamp'] = notification['timestamp'].strftime("%a, %d %b %Y %H:%M:%S GMT")
    return jsonify(notifications)

if __name__ == '__main__':
    app.run(debug=True)
