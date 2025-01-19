// File input handling
document.querySelector('.file-input').addEventListener('change', function(e) {
    const fileName = e.target.files[0]?.name;
    const fileNameDisplay = document.getElementById('file-name');
    const fileLabel = document.getElementById('file-label-text');
    
    if (fileName) {
        fileNameDisplay.textContent = `Selected file: ${fileName}`;
        fileNameDisplay.style.display = 'block';
        fileLabel.textContent = 'Change file';
    }
});

// Form submission handling
document.querySelector('form').addEventListener('submit', function() {
    document.getElementById('loading').style.display = 'block';
    document.querySelector('.submit-btn').disabled = true;
});

// Drag and drop handling
const dropZone = document.querySelector('.file-input-label');

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults (e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, unhighlight, false);
});

function highlight(e) {
    dropZone.style.borderColor = '#4CAF50';
    dropZone.style.backgroundColor = '#e8f5e9';
}

function unhighlight(e) {
    dropZone.style.borderColor = '#ddd';
    dropZone.style.backgroundColor = '#f8f9fa';
}

dropZone.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    document.querySelector('.file-input').files = files;
    
    const event = new Event('change');
    document.querySelector('.file-input').dispatchEvent(event);
}