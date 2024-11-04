from flask import Flask, jsonify, render_template
from pymongo import MongoClient

# Initialize Flask app
app = Flask(__name__)

# MongoDB client setup
client = MongoClient("mongodb://localhost:27017/")
db = client.monitoring_app

# Route to render the main HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to get metrics data
@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    metrics = list(db.metrics.find({}, {'_id': 0}))
    return jsonify(metrics)

# Route to get notifications data
@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    notifications = list(db.notifications.find({}, {'_id': 0}))
    return jsonify(notifications)

if __name__ == '__main__':
    app.run(debug=True)
