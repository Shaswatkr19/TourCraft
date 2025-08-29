// Dashboard JavaScript for dynamic features
document.addEventListener('DOMContentLoaded', function() {
    // Search functionality
    const searchInput = document.querySelector('input[placeholder="Search tours..."]');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            // Implement search logic
            console.log('Searching for:', this.value);
        });
    }
    
    // Create tour button
    const createTourBtn = document.querySelector('.login-btn, button[class*="primary"]');
    if (createTourBtn) {
        createTourBtn.addEventListener('click', function(e) {
            if (this.textContent.includes('Create')) {
                window.location.href = '/tours/create/';
            }
        });
    }
    
    // Tour actions (view, edit, delete)
    document.querySelectorAll('[data-tour-action]').forEach(button => {
        button.addEventListener('click', function() {
            const action = this.dataset.tourAction;
            const tourId = this.dataset.tourId;
            
            switch(action) {
                case 'view':
                    window.location.href = `/tours/${tourId}/`;
                    break;
                case 'edit':
                    window.location.href = `/tours/${tourId}/edit/`;
                    break;
                case 'delete':
                    if (confirm('Are you sure you want to delete this tour?')) {
                        // Implement delete functionality
                    }
                    break;
            }
        });
    });
});