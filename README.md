# System Monitoring Dashboard

A robust web application for real-time system monitoring, built with Python Flask, MongoDB, and JavaScript.

![Monitoring Dashboard](https://github.com/SalvatoreBevilacqua/monitoring_app/raw/main/screenshot.png)

## Technologies Used

- **Backend**: Python 3.11, Flask, PyMongo  
- **Database**: MongoDB  
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js, Bootstrap 5  
- **Containerization**: Docker, Docker Compose  
- **Development Tools**: Pipenv for dependency management

## Architecture

The application follows a three-tier architecture:

1. **Presentation Layer**: Responsive Bootstrap-based frontend with dynamic visualizations  
2. **Logic Layer**: Flask REST API for request handling and data processing  
3. **Data Layer**: MongoDB database for persistent storage

## Requirements

- Python 3.11  
- MongoDB 5.0 or higher  
- Docker and Docker Compose (optional, for containerized deployment)

## Installation

### Method 1: Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SalvatoreBevilacqua/monitoring_app.git
   cd monitoring_app
   ```

2. Install dependencies using Pipenv:
   ```bash
   pipenv install
   ```

3. Start MongoDB (if not already running):
   ```bash
   mongod --dbpath /path/to/data/directory
   ```

4. Generate test data:
   ```bash
   pipenv run python generate_data.py
   ```

5. Start the application:
   ```bash
   pipenv run python app.py
   ```

6. Access the application in your browser at [http://localhost:5000](http://localhost:5000)

---

### Method 2: Using Docker

1. Clone the repository:
   ```bash
   git clone https://github.com/SalvatoreBevilacqua/monitoring_app.git
   cd monitoring_app
   ```

2. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

3. Generate test data:
   ```bash
   docker-compose --profile data-generation up data-generator
   ```

4. Access the application in your browser at [http://localhost:5000](http://localhost:5000)

## Project Structure

```
monitoring_app/
├── app.py                 # Main Flask application
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── generate_data.py       # Script to generate test data
├── Pipfile                # Python dependency management
├── Pipfile.lock           # Locked dependencies
├── README.md              # Documentation
├── static/                # Static assets
│   └── scripts.js         # Frontend JavaScript code
└── templates/             # HTML templates
    └── index.html         # Main application page
```

## API Reference

### Available Endpoints

#### `GET /api/metrics`  
Returns system metrics with pagination and filtering support.  
**Query Parameters:**
- `page`: Page number (default: 1)  
- `per_page`: Items per page (default: 10)  
- `start_date`: Filter from this date (format YYYY-MM-DD)  
- `end_date`: Filter to this date (format YYYY-MM-DD)  
- `keyword`: Filter by keyword in activity  

#### `GET /api/notifications`  
Returns system notifications with pagination and filtering support.  
**Query Parameters:** Same as `/api/metrics`

#### `GET /api/metrics/summary`  
Returns a summary of system metrics.  
**Query Parameters:**
- `days`: Number of days for the summary (default: 30)

#### `GET /api/health`  
Returns the health status of the system and its components.

## Advanced Features

### Security

- Server-side validation of query parameters  
- Secure error handling  
- Comprehensive event logging  
- Environment variables for sensitive configurations

### Performance

- Pagination for handling large datasets  
- MongoDB query optimization  
- Containerization for scalable deployment

### Usability

- Intuitive user interface  
- Immediate visual feedback  
- Interactive charts for data analysis  
- Advanced filters for quickly finding information

## Project Strengths

- **Robust Architecture**: Clear separation between frontend, backend, and database  
- **RESTful API**: Well-designed interface for easy integration  
- **Docker-ready**: Complete configuration for containerized deployment  
- **Optimized Performance**: Server-side pagination and filtering  
- **Error Handling**: Comprehensive logging and error management system

## License

MIT License

## Author

Salvatore Bevilacqua
