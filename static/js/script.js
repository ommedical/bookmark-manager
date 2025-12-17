// Form validation
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        });
    }, 5000);
    
    // URL validation for bookmark form
    const bookmarkForm = document.getElementById('bookmarkForm');
    if (bookmarkForm) {
        bookmarkForm.addEventListener('submit', function(e) {
            const urlInput = document.getElementById('url');
            const url = urlInput.value.trim();
            
            if (url && !url.startsWith('http://') && !url.startsWith('https://')) {
                urlInput.value = 'https://' + url;
            }
        });
    }
    
    // Quick search
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        let searchTimer;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimer);
            searchTimer = setTimeout(() => {
                if (this.value.trim()) {
                    window.location.href = `/search?q=${encodeURIComponent(this.value.trim())}`;
                } else {
                    window.location.href = '/dashboard';
                }
            }, 500);
        });
    }
});