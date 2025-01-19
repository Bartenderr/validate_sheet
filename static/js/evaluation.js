document.addEventListener('DOMContentLoaded', function() {
    // Add loading state to download button
    const downloadBtn = document.querySelector('.download-btn');
    downloadBtn.addEventListener('click', function() {
        this.classList.add('loading');
        this.innerHTML = `
            <span class="icon">⏳</span>
            Preparing Download...
        `;
        
        // Remove loading state after download starts (after 1 second)
        setTimeout(() => {
            this.classList.remove('loading');
            this.innerHTML = `
                <span class="icon">📊</span>
                Download Evaluated Document
            `;
        }, 1000);
    });

    // Add hover effect to success icon
    const successIcon = document.querySelector('.success-icon');
    successIcon.addEventListener('mouseover', function() {
        this.style.transform = 'scale(1.1)';
    });
    successIcon.addEventListener('mouseout', function() {
        this.style.transform = 'scale(1)';
    });
});