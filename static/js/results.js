// Handle file input for standardized file upload
document.querySelector('.file-input').addEventListener('change', function(e) {
    const fileName = e.target.files[0]?.name;
    const fileNameDisplay = document.getElementById('standardized-file-name');
    const fileLabel = document.getElementById('standardized-file-label');
    
    if (fileName) {
        fileNameDisplay.textContent = `Selected file: ${fileName}`;
        fileNameDisplay.style.display = 'block';
        fileLabel.textContent = 'Change file';
    }
});

// Add loading state to form submission
document.querySelector('.standardized-form').addEventListener('submit', function() {
    const submitButton = this.querySelector('.submit-btn');
    submitButton.disabled = true;
    submitButton.innerHTML = `
        <span class="loading-spinner"></span>
        Processing...
    `;
});

// Make tables sortable (optional enhancement)
document.querySelectorAll('table.data').forEach(table => {
    const headers = table.querySelectorAll('th');
    headers.forEach(header => {
        header.addEventListener('click', () => {
            const index = Array.from(header.parentElement.children).indexOf(header);
            sortTable(table, index);
        });
        header.style.cursor = 'pointer';
        header.title = 'Click to sort';
    });
});

function sortTable(table, column) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const isNumeric = !isNaN(rows[0].children[column].textContent.trim());
    
    rows.sort((a, b) => {
        const aValue = a.children[column].textContent.trim();
        const bValue = b.children[column].textContent.trim();
        
        if (isNumeric) {
            return parseFloat(aValue) - parseFloat(bValue);
        }
        return aValue.localeCompare(bValue);
    });
    
    tbody.innerHTML = '';
    rows.forEach(row => tbody.appendChild(row));
}