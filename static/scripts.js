// Global variables
let currentMetricsPage = 1;
let currentNotificationsPage = 1;
const ITEMS_PER_PAGE = 10;
let metricsChartInstance = null;
let usersChartInstance = null;

// DOM Elements
document.addEventListener("DOMContentLoaded", function () {
    // Initialize the app
    initApp();
    
    // Set up event listeners
    setupEventListeners();
    
    // Initialize charts
    initCharts();
});

/**
 * Initialize the application
 */
function initApp() {
    loadDashboardSummary();
    loadTables();
    updateHealthStatus();
    
    // Initialize tooltips
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

/**
 * Set up event listeners for interactive elements
 */
function setupEventListeners() {
    // Filter form submission
    document.getElementById('filter-form').addEventListener('submit', function(e) {
        e.preventDefault();
        applyFilters();
    });
    
    // Reset filters button
    document.getElementById('reset-filters').addEventListener('click', resetFilters);
    
    // Page navigation buttons for metrics
    document.getElementById('metrics-prev').addEventListener('click', function() {
        if (currentMetricsPage > 1) {
            currentMetricsPage--;
            loadMetricsTable();
        }
    });
    
    document.getElementById('metrics-next').addEventListener('click', function() {
        currentMetricsPage++;
        loadMetricsTable();
    });
    
    // Page navigation buttons for notifications
    document.getElementById('notifications-prev').addEventListener('click', function() {
        if (currentNotificationsPage > 1) {
            currentNotificationsPage--;
            loadNotificationsTable();
        }
    });
    
    document.getElementById('notifications-next').addEventListener('click', function() {
        currentNotificationsPage++;
        loadNotificationsTable();
    });
    
    // Time range selector for summary
    document.getElementById('time-range').addEventListener('change', function() {
        loadDashboardSummary();
        refreshCharts();
    });
    
    // Refresh button
    document.getElementById('refresh-data').addEventListener('click', function() {
        this.classList.add('spin');
        refreshAllData().then(() => {
            setTimeout(() => {
                this.classList.remove('spin');
            }, 500);
        });
    });
}

/**
 * Initialize chart objects
 */
function initCharts() {
    // Uptime Chart
    const metricsCtx = document.getElementById('metrics-chart').getContext('2d');
    metricsChartInstance = new Chart(metricsCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Uptime %',
                data: [],
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1,
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: false,
                    min: 90,
                    max: 100
                }
            }
        }
    });
    
    // Users Chart
    const usersCtx = document.getElementById('users-chart').getContext('2d');
    usersChartInstance = new Chart(usersCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Connected Users',
                data: [],
                borderColor: 'rgb(54, 162, 235)',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                tension: 0.1,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
    
    // Load initial chart data
    refreshCharts();
}

/**
 * Refresh all charts with latest data
 */
async function refreshCharts() {
    try {
        const days = document.getElementById('time-range').value;
        const response = await fetch(`/api/metrics?per_page=100&page=1`);
        const data = await response.json();
        
        if (data && data.data) {
            updateMetricsChart(data.data);
            updateUsersChart(data.data);
        }
    } catch (error) {
        console.error('Error loading chart data:', error);
        showToast('Error loading chart data', 'error');
    }
}

/**
 * Update the uptime metrics chart
 */
function updateMetricsChart(data) {
    // Sort by timestamp
    const sortedData = [...data].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
    
    // Get the last 30 entries
    const chartData = sortedData.slice(-30);
    
    const labels = chartData.map(item => {
        const date = new Date(item.timestamp);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    });
    
    const uptimeData = chartData.map(item => item.uptime);
    
    metricsChartInstance.data.labels = labels;
    metricsChartInstance.data.datasets[0].data = uptimeData;
    metricsChartInstance.update();
}

/**
 * Update the users chart
 */
function updateUsersChart(data) {
    // Sort by timestamp
    const sortedData = [...data].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
    
    // Get the last 30 entries
    const chartData = sortedData.slice(-30);
    
    const labels = chartData.map(item => {
        const date = new Date(item.timestamp);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    });
    
    const usersData = chartData.map(item => item.users_connected);
    
    usersChartInstance.data.labels = labels;
    usersChartInstance.data.datasets[0].data = usersData;
    usersChartInstance.update();
}

/**
 * Refresh all data on the dashboard
 */
async function refreshAllData() {
    try {
        await Promise.all([
            loadDashboardSummary(),
            loadTables(),
            updateHealthStatus(),
            refreshCharts()
        ]);
        showToast('Data refreshed successfully', 'success');
    } catch (error) {
        console.error('Error refreshing data:', error);
        showToast('Error refreshing data', 'error');
    }
}

/**
 * Load the dashboard summary data
 */
async function loadDashboardSummary() {
    try {
        const days = document.getElementById('time-range').value;
        const response = await fetch(`/api/metrics/summary?days=${days}`);
        const data = await response.json();
        
        if (data) {
            document.getElementById('avg-uptime').textContent = data.avg_uptime + '%';
            document.getElementById('max-users').textContent = data.max_concurrent_users;
            document.getElementById('avg-users').textContent = Math.round(data.avg_users);
            document.getElementById('suspicious-count').textContent = data.suspicious_activities;
            
            // Update the progress bar
            const uptimeBar = document.getElementById('uptime-progress');
            uptimeBar.style.width = data.avg_uptime + '%';
            uptimeBar.setAttribute('aria-valuenow', data.avg_uptime);
            
            // Set classes based on uptime value
            if (data.avg_uptime >= 99) {
                uptimeBar.className = 'progress-bar bg-success';
            } else if (data.avg_uptime >= 95) {
                uptimeBar.className = 'progress-bar bg-info';
            } else if (data.avg_uptime >= 90) {
                uptimeBar.className = 'progress-bar bg-warning';
            } else {
                uptimeBar.className = 'progress-bar bg-danger';
            }
        }
    } catch (error) {
        console.error('Error loading dashboard summary:', error);
        showToast('Error loading summary data', 'error');
    }
}

/**
 * Load both data tables
 */
async function loadTables() {
    await Promise.all([
        loadMetricsTable(),
        loadNotificationsTable()
    ]);
}

/**
 * Fetch and display metrics data with pagination
 */
async function loadMetricsTable() {
    try {
        const startDate = document.getElementById('start-date').value;
        const endDate = document.getElementById('end-date').value;
        const keyword = document.getElementById('search-keyword').value.trim();
        
        let url = `/api/metrics?page=${currentMetricsPage}&per_page=${ITEMS_PER_PAGE}`;
        
        if (startDate) url += `&start_date=${startDate}`;
        if (endDate) url += `&end_date=${endDate}`;
        if (keyword) url += `&keyword=${encodeURIComponent(keyword)}`;
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data && data.data) {
            populateTable(data.data, 'metrics-table');
            updatePagination(data.pagination, 'metrics');
        }
    } catch (error) {
        console.error('Error loading metrics data:', error);
        showToast('Error loading metrics data', 'error');
    }
}

/**
 * Fetch and display notifications data with pagination
 */
async function loadNotificationsTable() {
    try {
        const startDate = document.getElementById('start-date').value;
        const endDate = document.getElementById('end-date').value;
        const keyword = document.getElementById('search-keyword').value.trim();
        
        let url = `/api/notifications?page=${currentNotificationsPage}&per_page=${ITEMS_PER_PAGE}`;
        
        if (startDate) url += `&start_date=${startDate}`;
        if (endDate) url += `&end_date=${endDate}`;
        if (keyword) url += `&keyword=${encodeURIComponent(keyword)}`;
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data && data.data) {
            populateTable(data.data, 'notifications-table');
            updatePagination(data.pagination, 'notifications');
        }
    } catch (error) {
        console.error('Error loading notifications data:', error);
        showToast('Error loading notifications data', 'error');
    }
}

/**
 * Update the pagination controls based on data
 */
function updatePagination(pagination, tableType) {
    const currentPage = pagination.page;
    const totalPages = pagination.pages;
    
    document.getElementById(`${tableType}-page-info`).textContent = 
        `Page ${currentPage} of ${totalPages || 1} (${pagination.total} total records)`;
    
    // Update previous button state
    const prevButton = document.getElementById(`${tableType}-prev`);
    if (currentPage <= 1) {
        prevButton.classList.add('disabled');
    } else {
        prevButton.classList.remove('disabled');
    }
    
    // Update next button state
    const nextButton = document.getElementById(`${tableType}-next`);
    if (currentPage >= totalPages) {
        nextButton.classList.add('disabled');
    } else {
        nextButton.classList.remove('disabled');
    }
}

/**
 * Populate table with data
 */
function populateTable(data, tableId) {
    const tableBody = document.querySelector(`#${tableId} tbody`);
    tableBody.innerHTML = '';
    
    if (data.length === 0) {
        const row = document.createElement('tr');
        const cell = document.createElement('td');
        cell.colSpan = tableId === 'metrics-table' ? 4 : 3;
        cell.textContent = 'No data found';
        cell.className = 'text-center';
        row.appendChild(cell);
        tableBody.appendChild(row);
        return;
    }
    
    data.forEach(item => {
        const row = document.createElement('tr');
        
        if (tableId === 'metrics-table') {
            // Format the date
            const timestamp = new Date(item.timestamp).toLocaleString();
            
            // Create cells
            row.innerHTML = `
                <td>${timestamp}</td>
                <td>
                    <div class="progress" style="height: 20px;">
                        <div class="progress-bar ${getUptimeClass(item.uptime)}" 
                             role="progressbar" 
                             style="width: ${item.uptime}%" 
                             aria-valuenow="${item.uptime}" 
                             aria-valuemin="0" 
                             aria-valuemax="100">
                            ${item.uptime}%
                        </div>
                    </div>
                </td>
                <td>${item.users_connected}</td>
                <td>
                    <span class="badge ${item.activity === 'Suspicious' ? 'bg-danger' : 'bg-success'}">
                        ${item.activity}
                    </span>
                </td>
            `;
        } else {
            // Format the date for notifications
            const timestamp = new Date(item.timestamp).toLocaleString();
            
            // Create cells
            row.innerHTML = `
                <td>${timestamp}</td>
                <td>
                    <span class="badge bg-warning text-dark">
                        ${item.event_type}
                    </span>
                </td>
                <td>${item.description}</td>
            `;
        }
        
        tableBody.appendChild(row);
    });
}

/**
 * Get the appropriate Bootstrap class for uptime percentage
 */
function getUptimeClass(uptime) {
    if (uptime >= 99) return 'bg-success';
    if (uptime >= 95) return 'bg-info';
    if (uptime >= 90) return 'bg-warning';
    return 'bg-danger';
}

/**
 * Apply filters to both tables
 */
function applyFilters() {
    // Reset pagination to first page when filters are applied
    currentMetricsPage = 1;
    currentNotificationsPage = 1;
    
    loadTables();
    refreshCharts();
}

/**
 * Reset all filters
 */
function resetFilters() {
    document.getElementById('start-date').value = '';
    document.getElementById('end-date').value = '';
    document.getElementById('search-keyword').value = '';
    
    // Reset pagination
    currentMetricsPage = 1;
    currentNotificationsPage = 1;
    
    loadTables();
    refreshCharts();
}

/**
 * Check and update system health status
 */
async function updateHealthStatus() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        
        const statusElement = document.getElementById('health-status');
        const statusIconElement = document.getElementById('health-status-icon');
        
        if (data.status === 'healthy') {
            statusElement.textContent = 'Healthy';
            statusElement.className = 'badge bg-success';
            statusIconElement.className = 'fas fa-check-circle text-success';
            
            // Update last checked time
            document.getElementById('last-health-check').textContent = 
                `Last checked: ${new Date().toLocaleTimeString()}`;
        } else {
            statusElement.textContent = 'Unhealthy';
            statusElement.className = 'badge bg-danger';
            statusIconElement.className = 'fas fa-exclamation-circle text-danger';
            
            // Show error details
            console.error('Health check failed:', data.error);
        }
    } catch (error) {
        console.error('Error checking system health:', error);
        
        // Update UI to show error
        const statusElement = document.getElementById('health-status');
        statusElement.textContent = 'Error';
        statusElement.className = 'badge bg-danger';
        
        const statusIconElement = document.getElementById('health-status-icon');
        statusIconElement.className = 'fas fa-exclamation-circle text-danger';
    }
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container');
    
    // Create toast element
    const toastElement = document.createElement('div');
    toastElement.className = `toast align-items-center border-0 ${type === 'error' ? 'bg-danger' : 'bg-success'} text-white`;
    toastElement.setAttribute('role', 'alert');
    toastElement.setAttribute('aria-live', 'assertive');
    toastElement.setAttribute('aria-atomic', 'true');
    
    // Create toast content
    toastElement.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    // Add to container
    toastContainer.appendChild(toastElement);
    
    // Initialize and show toast
    const toast = new bootstrap.Toast(toastElement, {
        delay: 3000
    });
    toast.show();
    
    // Remove toast after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}