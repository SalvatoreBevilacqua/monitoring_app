from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime, timedelta
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MongoDB client setup with connection string from environment variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "monitoring_app")

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    # Test connection
    client.admin.command('ping')
    logger.info("Successfully connected to MongoDB")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    raise

# Route to render the main HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Helper function to parse date parameters
def parse_date_param(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None

# API route for metrics data with pagination and filtering
@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    try:
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        start_date = parse_date_param(request.args.get('start_date'))
        end_date = parse_date_param(request.args.get('end_date'))
        keyword = request.args.get('keyword', '')
        
        # Build query
        query = {}
        if start_date or end_date:
            query['timestamp'] = {}
            if start_date:
                query['timestamp']['$gte'] = start_date
            if end_date:
                # Include the entire end date
                query['timestamp']['$lte'] = end_date + timedelta(days=1) - timedelta(seconds=1)
        
        if keyword:
            query['activity'] = {'$regex': keyword, '$options': 'i'}
        
        # Get total count for pagination
        total = db.metrics.count_documents(query)
        
        # Fetch paginated data
        metrics = list(db.metrics.find(
            query, 
            {'_id': 0}
        ).sort('timestamp', -1).skip((page - 1) * per_page).limit(per_page))
        
        # Format timestamps
        for metric in metrics:
            metric['timestamp'] = metric['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        
        return jsonify({
            'data': metrics,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        })
    except Exception as e:
        logger.error(f"Error fetching metrics: {e}")
        return jsonify({'error': 'Failed to fetch metrics'}), 500

# API route for notifications data with pagination and filtering
@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    try:
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        start_date = parse_date_param(request.args.get('start_date'))
        end_date = parse_date_param(request.args.get('end_date'))
        keyword = request.args.get('keyword', '')
        
        # Build query
        query = {}
        if start_date or end_date:
            query['timestamp'] = {}
            if start_date:
                query['timestamp']['$gte'] = start_date
            if end_date:
                # Include the entire end date
                query['timestamp']['$lte'] = end_date + timedelta(days=1) - timedelta(seconds=1)
        
        if keyword:
            query['$or'] = [
                {'event_type': {'$regex': keyword, '$options': 'i'}},
                {'description': {'$regex': keyword, '$options': 'i'}}
            ]
        
        # Get total count for pagination
        total = db.notifications.count_documents(query)
        
        # Fetch paginated data
        notifications = list(db.notifications.find(
            query, 
            {'_id': 0}
        ).sort('timestamp', -1).skip((page - 1) * per_page).limit(per_page))
        
        # Format timestamps
        for notification in notifications:
            notification['timestamp'] = notification['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        
        return jsonify({
            'data': notifications,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        })
    except Exception as e:
        logger.error(f"Error fetching notifications: {e}")
        return jsonify({'error': 'Failed to fetch notifications'}), 500

# API for system health status
@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        # Check MongoDB connection
        client.admin.command('ping')
        
        # Get server stats
        uptime = db.command('serverStatus')['uptime']
        
        # Get some application metrics
        metrics_count = db.metrics.count_documents({})
        notifications_count = db.notifications.count_documents({})
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'db_uptime_seconds': uptime,
            'metrics_count': metrics_count,
            'notifications_count': notifications_count,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }), 500

# API for metrics summary/analytics
@app.route('/api/metrics/summary', methods=['GET'])
def metrics_summary():
    try:
        # Get time range parameters
        days = int(request.args.get('days', 30))
        if days <= 0 or days > 365:
            days = 30  # Default to 30 days if invalid
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Query metrics within date range
        query = {'timestamp': {'$gte': start_date, '$lte': end_date}}
        
        # Get all metrics in time range
        metrics = list(db.metrics.find(query, {'_id': 0}))
        
        # Calculate average uptime
        if metrics:
            avg_uptime = sum(metric['uptime'] for metric in metrics) / len(metrics)
        else:
            avg_uptime = 0
        
        # Count suspicious activities
        suspicious_count = db.metrics.count_documents({
            'timestamp': {'$gte': start_date, '$lte': end_date},
            'activity': 'Suspicious'
        })
        
        # Get max concurrent users
        max_users = 0
        if metrics:
            max_users = max(metric['users_connected'] for metric in metrics)
        
        # Get average users
        if metrics:
            avg_users = sum(metric['users_connected'] for metric in metrics) / len(metrics)
        else:
            avg_users = 0
        
        return jsonify({
            'period_days': days,
            'total_records': len(metrics),
            'avg_uptime': round(avg_uptime, 2),
            'suspicious_activities': suspicious_count,
            'max_concurrent_users': max_users,
            'avg_users': round(avg_users, 2),
            'data_start': start_date.strftime("%Y-%m-%d"),
            'data_end': end_date.strftime("%Y-%m-%d")
        })
    except Exception as e:
        logger.error(f"Error generating metrics summary: {e}")
        return jsonify({'error': 'Failed to generate metrics summary'}), 500

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server error: {e}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=os.environ.get('DEBUG', 'False').lower() == 'true', host='0.0.0.0', port=port)