let metricsData = [];         // Global variable to hold metrics data
let notificationsData = [];   // Global variable to hold notifications data

document.addEventListener("DOMContentLoaded", function () {
    loadTables();  // Load initial data on page load
});

async function fetchData(url) {
    const response = await fetch(url);
    return response.json();
}

function populateTable(data, tableId) {
const tableBody = document.querySelector(`#${tableId} tbody`);
tableBody.innerHTML = '';  // Clear existing data
data.forEach(item => {
    const row = document.createElement('tr');
    
    // Ensure the order for Notifications table is correct
    if (tableId === 'notifications-table') {
        row.innerHTML = `<td>${item.timestamp}</td><td>${item.event_type}</td><td>${item.description}</td>`;
        } else {
            row.innerHTML = `<td>${item.timestamp}</td><td>${item.uptime}</td><td>${item.users_connected}</td><td>${item.activity}</td>`;
        }

    tableBody.appendChild(row);
});
}

async function loadTables() {
    // Fetch data and store in global variables
    metricsData = await fetchData('http://127.0.0.1:5000/api/metrics');
    notificationsData = await fetchData('http://127.0.0.1:5000/api/notifications');
    
    // Populate tables with initial data
    populateTable(metricsData, 'metrics-table');
    populateTable(notificationsData, 'notifications-table');
}

function applyFilters() {
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    const keyword = document.getElementById('search-keyword').value.toLowerCase();

    // Filter metrics data
    const filteredMetrics = metricsData.filter(item => {
        const rowDate = new Date(item.timestamp).toISOString().slice(0, 10);
        const startDateMatch = startDate ? rowDate >= startDate : true;
        const endDateMatch = endDate ? rowDate <= endDate : true;
        const keywordMatch = !keyword || item.activity.toLowerCase().includes(keyword);
        return startDateMatch && endDateMatch && keywordMatch;
    });

    // Filter notifications data
    const filteredNotifications = notificationsData.filter(item => {
        const rowDate = new Date(item.timestamp).toISOString().slice(0, 10);
        const startDateMatch = startDate ? rowDate >= startDate : true;
        const endDateMatch = endDate ? rowDate <= endDate : true;
        const keywordMatch = !keyword || item.description.toLowerCase().includes(keyword);
        return startDateMatch && endDateMatch && keywordMatch;
    });

    // Populate tables with filtered data
    populateTable(filteredMetrics, 'metrics-table');
    populateTable(filteredNotifications, 'notifications-table');
}

function resetFilters() {
    document.getElementById('start-date').value = '';
    document.getElementById('end-date').value = '';
    document.getElementById('search-keyword').value = '';
    populateTable(metricsData, 'metrics-table');  // Reset to original data
    populateTable(notificationsData, 'notifications-table');
}