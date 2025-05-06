# 📊 System Monitoring Dashboard

> A robust web application for real-time system monitoring, built with Python Flask, MongoDB, and JavaScript.

![License](https://img.shields.io/badge/license-MIT-green)
![Python Version](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.3-blue)
![MongoDB](https://img.shields.io/badge/MongoDB-5.0+-yellow)
![Deployment](https://img.shields.io/badge/Deployment-Docker-blue?logo=docker)

![Dashboard](https://github.com/SalvatoreBevilacqua/monitoring_app/raw/main/screenshot.png)

---

## 🚀 Features

- **Real-time System Monitoring**: Track uptime, user connections, and system activity
- **Interactive Visualizations**: Dynamic charts powered by Chart.js
- **Detailed Analytics**: Summary statistics and trend analysis
- **Alert Management**: Notification system for suspicious activities
- **Responsive Design**: Bootstrap 5 mobile-first interface
- **Advanced Filtering**: Date range and keyword search capabilities
- **RESTful API**: Well-documented endpoints for system integration
- **Containerized Deployment**: Docker and Docker Compose support

---

## 🛠️ Tech Stack

| Layer           | Technologies                                         |
|-----------------|------------------------------------------------------|
| **Backend**     | Python 3.11, Flask, PyMongo                          |
| **Frontend**    | HTML5, CSS3, JavaScript, Chart.js, Bootstrap 5       |
| **Database**    | MongoDB                                              |
| **Deployment**  | Docker, Docker Compose                               |
| **Tools**       | Pipenv for dependency management                     |
| **Monitoring**  | Custom metrics collection and visualization          |

---

## 📦 Installation & Setup

### Method 1: Manual Installation

```bash
git clone https://github.com/SalvatoreBevilacqua/monitoring_app.git
cd monitoring_app
pipenv install
```

### 🔐 Environment Variables

Create a `.env` file and add:

```env
MONGO_URI=mongodb://localhost:27017/
DB_NAME=monitoring_app
DEBUG=False
PORT=5000
```

### Starting MongoDB

```bash
mongod --dbpath /path/to/data/directory
```

### Generate Test Data

```bash
pipenv run generate
```

### Run the Application

```bash
pipenv run start
```

---

### Method 2: Using Docker

```bash
git clone https://github.com/SalvatoreBevilacqua/monitoring_app.git
cd monitoring_app
docker-compose up -d
```

### Generate Test Data with Docker

```bash
docker-compose --profile data-generation up data-generator
```

---

## 🔄 API Reference

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

---

## 📁 Project Structure

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

---

## 🧪 Testing

Tested on:

- ✅ Desktop: Chrome, Firefox, Safari
- ✅ Mobile: Android Chrome, iOS Safari
- ✅ Devices: Responsive on phones and tablets

To run tests:

```bash
pipenv run test
```

---

## 🌍 Deployment

### Docker Deployment Steps:

1. Ensure Docker and Docker Compose are installed
2. Update environment variables in docker-compose.yml if needed
3. Run `docker-compose up -d` to start the application
4. Access the dashboard at http://localhost:5000

### Manual Deployment:

1. Set up a MongoDB instance
2. Configure environment variables for production
3. Use Gunicorn as WSGI server:
   ```bash
   pipenv run gunicorn -b 0.0.0.0:5000 app:app
   ```

---

## 🔮 Future Enhancements

- User authentication system
- Role-based access control
- Email alerting for critical events
- Additional visualization options
- Historical data analysis
- API key management for external integrations
- Dark mode support

---

## 🙏 Credits

- [Flask](https://flask.palletsprojects.com/)
- [MongoDB](https://www.mongodb.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Chart.js](https://www.chartjs.org/)
- [Font Awesome](https://fontawesome.com/)

---

## 📜 License

MIT License

---

## 👨‍💻 Author

**Salvatore Bevilacqua**  
[GitHub](https://github.com/SalvatoreBevilacqua) • [LinkedIn](https://linkedin.com/in/salvatore-bevilacqua)
