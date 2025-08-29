// API wrapper for TourCraft backend
class TourCraftAPI {
    constructor() {
        this.baseURL = '/api/';
        this.authToken = localStorage.getItem('authToken');
    }
    
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken(),
                ...options.headers
            },
            ...options
        };
        
        if (this.authToken) {
            config.headers['Authorization'] = `Bearer ${this.authToken}`;
        }
        
        try {
            const response = await fetch(url, config);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }
    
    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    }
    
    // Tours API
    async getTours() {
        return this.request('tours/');
    }
    
    async createTour(tourData) {
        return this.request('tours/', {
            method: 'POST',
            body: JSON.stringify(tourData)
        });
    }
    
    async updateTour(id, tourData) {
        return this.request(`tours/${id}/`, {
            method: 'PATCH',
            body: JSON.stringify(tourData)
        });
    }
    
    async deleteTour(id) {
        return this.request(`tours/${id}/`, {
            method: 'DELETE'
        });
    }
    
    async getDashboardStats() {
        return this.request('tours/dashboard_stats/');
    }
    
    // Tour Steps API
    async addTourStep(tourId, stepData) {
        return this.request(`tours/${tourId}/add_step/`, {
            method: 'POST',
            body: JSON.stringify(stepData)
        });
    }
}

// Usage example:
const api = new TourCraftAPI();

// Load dashboard data
async function loadDashboardData() {
    try {
        const stats = await api.getDashboardStats();
        updateDashboardUI(stats);
    } catch (error) {
        console.error('Failed to load dashboard data:', error);
    }
}

function updateDashboardUI(stats) {
    // Update stats cards
    document.querySelector('[data-stat="tours"]').textContent = stats.total_tours;
    document.querySelector('[data-stat="published"]').textContent = stats.published_tours;
    document.querySelector('[data-stat="views"]').textContent = stats.total_views;
    
    // Update tours table
    const toursTable = document.querySelector('#tours-table tbody');
    if (toursTable && stats.recent_tours) {
        toursTable.innerHTML = stats.recent_tours.map(tour => `
            <tr class="hover:bg-gray-50">
                <td class="px-6 py-4">
                    <div class="flex items-center">
                        <div class="h-8 w-8 rounded-lg bg-primary-100 flex items-center justify-center">
                            <svg class="h-4 w-4 text-primary-600">...</svg>
                        </div>
                        <div class="ml-3">
                            <p class="text-sm font-semibold text-gray-900">${tour.title}</p>
                            <p class="text-sm text-gray-500">${tour.steps_count} steps</p>
                        </div>
                    </div>
                </td>
                <td class="px-6 py-4">
                    <span class="px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusClass(tour.status)}">
                        ${tour.status}
                    </span>
                </td>
                <td class="px-6 py-4 text-sm text-gray-900">${tour.view_count}</td>
                <td class="px-6 py-4 text-sm text-gray-500">${tour.updated_ago}</td>
                <td class="px-6 py-4">
                    <div class="flex items-center justify-end gap-2">
                        <button onclick="viewTour('${tour.id}')" class="text-gray-400 hover:text-gray-600">
                            <svg class="w-4 h-4">...</svg>
                        </button>
                        <button onclick="editTour('${tour.id}')" class="text-gray-400 hover:text-gray-600">
                            <svg class="w-4 h-4">...</svg>
                        </button>
                        <button onclick="deleteTour('${tour.id}')" class="text-gray-400 hover:text-gray-600">
                            <svg class="w-4 h-4">...</svg>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');
    }
}

function getStatusClass(status) {
    const classes = {
        'Published': 'bg-emerald-100 text-emerald-800',
        'Draft': 'bg-yellow-100 text-yellow-800',
        'Archived': 'bg-gray-100 text-gray-800'
    };
    return classes[status] || classes['Draft'];
}